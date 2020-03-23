<template>
  <v-container id="count-statistics" class="pt-0">
    <v-row>
      <v-col v-if="$vuetify.breakpoint.smAndUp" sm="1" md="1"></v-col>
      <v-col cols="5" sm="3" md="2">
        <v-text-field
          v-model="lastest"
          prefix="最近"
          suffix="期"
          single-line
          hide-details
          class="text-field-center"
          @change="lastestChanged()"
        ></v-text-field>
      </v-col>
      <v-col v-if="$vuetify.breakpoint.smAndUp" sm="1" md="2"></v-col>
      <v-col cols="7"></v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="6">
        <v-card>
          <bar-chart
            :chartRef="barChartRef"
            :xAxisName="barChartXAxisName"
            :xAxisData="barChartXAxisData"
            :yAxisName="barChartYAxisName"
            :data="barChartData"
          ></bar-chart>
        </v-card>
      </v-col>
      <v-col cols="12" md="6">
        <v-card>
          <pie-chart :chartRef="pieChartRef" :legendData="pieChartLegendData" :data="pieChartData"></pie-chart>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-data-table
            :headers="vuetifyTableData.headers"
            :items="vuetifyTableData.items"
            :items-per-page="10"
            :search="search"
            :loading="loading"
            :dense="denseTable"
            class="table-with-border"
          >
            <template v-slot:top>
              <v-btn
                class="mt-4 mb-4 ml-3 ml-sm-10"
                outlined
                rounded
                color="primary"
                @click="denseTable = !denseTable"
              >{{ btnText }}</v-btn>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import BarChart from "../components/BarChart";
import PieChart from "../components/PieChart";

export default {
  components: {
    BarChart,
    PieChart
  },
  data() {
    return {
      search: "",
      loading: true,
      denseTable: false,
      lastest: -1, // 只显示最近 lastest 期。
      vuetifyTableData: {
        headers: [],
        items: []
      },

      barChartRef: "countStatisticsBarChart",
      barChartXAxisName: "次数",
      barChartXAxisData: [],
      barChartYAxisName: "个数",
      barChartData: [],

      pieChartRef: "countStatisticsPieChart",
      pieChartLegendData: [],
      pieChartData: []
    };
  },
  computed: {
    allData() {
      return this.$store.state.allData;
    },
    winningNumberList() {
      return this.$store.state.winningNumberList;
    },
    btnText() {
      return this.denseTable == true ? "关闭密集模式" : "开启密集模式";
    }
  },
  watch: {
    allData: {
      handler() {
        this.setData();
      },
      deep: true // watch 默认无法监听对象内部的变化，将 deep 设为 true 就可以监听了
      // immediate: true  // 将该属性设为 true，组件在被创建时会自动执行 handler 一次。
      // 但由于 this.allData 的数据量很大，使用该属性会导致页面卡顿，所以改为在 created 函数中实现此功能
    }
  },
  created() {
    if (this.allData.length != 0) this.setData();
  },
  methods: {
    setData() {
      this.loading = false;
      this.lastestChanged();
    },
    lastestChanged() {
      if (this.lastest < 0 || this.lastest > this.allData.length)
        this.lastest = this.allData.length;

      /* 准备数据 */
      let winningCount = {}; // 号码-次数 字典
      let countNumber = {}; // 次数-个数 字典
      for (let i = 0; i < this.lastest; i++) {
        let item = this.winningNumberList[i];
        if (winningCount[item]) winningCount[item]++;
        else winningCount[item] = 1;
      }
      for (let i in winningCount) {
        if (countNumber[winningCount[i]]) countNumber[winningCount[i]]++;
        else countNumber[winningCount[i]] = 1;
      }
      countNumber[0] = 1000 - Object.keys(winningCount).length; // 剩余的号码出现的次数都是 0

      /* 生成表格数据 */
      this.vuetifyTableData.headers = [];
      let counts = Object.keys(countNumber);
      for (let i of counts)
        this.vuetifyTableData.headers.push({
          text: i,
          align: "center",
          sortable: false,
          value: i
        });
      this.vuetifyTableData.items = [];
      for (let i = 0; i < this.lastest; i++) {
        let winningNo = this.winningNumberList[i];
        let item = {};
        for (let j of counts) item[j] = "";
        item[winningCount[winningNo]] = winningNo;
        this.vuetifyTableData.items.push(item);
      }

      /* bar chart 数据 */
      this.barChartXAxisData = counts;
      this.barChartData = Object.values(countNumber);

      /* pie chart 数据 */
      this.pieChartData = [];
      for (let i in countNumber) {
        let item = {};
        item["name"] = i;
        item["value"] = countNumber[i];
        this.pieChartData.push(item);
      }
      this.pieChartLegendData = counts;
    }
  }
};
</script>
