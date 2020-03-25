<template>
  <v-container id="calc-012" class="pt-0">
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

      barChartRef: "calc012BarChart",
      barChartXAxisName: "012路",
      barChartXAxisData: [],
      barChartYAxisName: "个数",
      barChartData: [],

      pieChartRef: "calc012PieChart",
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
      }
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
      let winningCalc012 = {}; // 号码-012路 字典
      let calc012Counter = {}; // 012路-个数 字典
      for (let i = 0; i < 3; i++)
        for (let j = 0; j < 3; j++)
          for (let k = 0; k < 3; k++) calc012Counter[String(i) + j + k] = 0; // 初始化 012路-个数 字典
      for (let i = 0; i < this.lastest; i++) {
        let item = this.winningNumberList[i];
        let numAttr = "";
        for (let char of item) numAttr += String(Number(char) % 3);
        calc012Counter[numAttr]++;
        winningCalc012[item] = numAttr;
      }

      /* 转换成双值子序列排个序，不然顺序是乱的 */
      let twoValuedSeq = Object.entries(calc012Counter); // calc012Counter 对应的双值子序列
      twoValuedSeq.sort((item1, item2) => {
        if (item1[0] > item2[0]) return 1;
        else if (item1[0] == item2[0]) return 0;
        else return -1;
      });

      /* 生成表格数据 */
      let calc012 = [];
      for (let item of twoValuedSeq) calc012.push(item[0]);
      this.vuetifyTableData.headers = [];
      for (let i of calc012) {
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
        for (let j of calc012) item[j] = "";
        item[winningCalc012[winningNo]] = winningNo;
        this.vuetifyTableData.items.push(item);
      }

      /* bar chart 数据 */
      this.barChartXAxisData = calc012;
      this.barChartData = [];
      for (let item of twoValuedSeq) this.barChartData.push(item[1]);

      /* pie chart 数据 */
      this.pieChartData = [];
      for (let i of twoValuedSeq) {
        let item = {};
        item["name"] = i[0];
        item["value"] = i[1];
        this.pieChartData.push(item);
      }
      this.pieChartLegendData = calc012;
    }
  }
};
</script>
