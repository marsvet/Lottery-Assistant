<template>
  <v-container id="calc-span" class="pt-0">
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
          <data-table
            :headers="vuetifyTableData.headers"
            :items="vuetifyTableData.items"
            :loading="tableLoading"
            :withBorder="true"
          ></data-table>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import BarChart from "../components/BarChart";
import PieChart from "../components/PieChart";
import DataTable from "../components/DataTable";

export default {
  components: {
    BarChart,
    PieChart,
    DataTable
  },
  data() {
    return {
      tableLoading: true,
      lastest: 100, // 只显示最近 lastest 期。
      vuetifyTableData: {
        headers: [],
        items: []
      },

      barChartRef: "calcSpanBarChart",
      barChartXAxisName: "跨度",
      barChartXAxisData: [],
      barChartYAxisName: "个数",
      barChartData: [],

      pieChartRef: "calcSpanPieChart",
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
      this.tableLoading = false;
      this.lastestChanged();
    },
    lastestChanged() {
      if (this.lastest < 0 || this.lastest > this.allData.length)
        this.lastest = this.allData.length;

      /* 准备数据 */
      let winningCalcSpan = {}; // 号码-跨度 字典
      let calcSpanCounter = {}; // 跨度-个数 字典
      for (let i = 0; i < 10; i++) calcSpanCounter[i] = 0; // 初始化 跨度-个数 字典
      for (let i = 0; i < this.lastest; i++) {
        let item = this.winningNumberList[i];
        let numAttr = Math.max(...item) - Math.min(...item); // ...Array : 数组解构，字符串也可
        calcSpanCounter[numAttr]++;
        winningCalcSpan[item] = numAttr;
      }

      /* 生成表格数据 */
      let calcSpan = Object.keys(calcSpanCounter);
      this.vuetifyTableData.headers = [];
      for (let i of calcSpan) {
        this.vuetifyTableData.headers.push({
          text: i,
          align: "center",
          sortable: false,
          value: i
        });
      }
      this.vuetifyTableData.items = [];
      for (let i = 0; i < this.lastest; i++) {
        let winningNo = this.winningNumberList[i];
        let item = {};
        for (let j of calcSpan) item[j] = "";
        item[winningCalcSpan[winningNo]] = winningNo;
        this.vuetifyTableData.items.push(item);
      }

      /* bar chart 数据 */
      this.barChartXAxisData = calcSpan;
      this.barChartData = Object.values(calcSpanCounter);

      /* pie chart 数据 */
      this.pieChartData = [];
      for (let i in calcSpanCounter) {
        let item = {};
        item["name"] = i;
        item["value"] = calcSpanCounter[i];
        this.pieChartData.push(item);
      }
      this.pieChartLegendData = calcSpan;
    }
  }
};
</script>
