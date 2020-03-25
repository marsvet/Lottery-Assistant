<template>
  <v-container id="calc-sum" class="pt-0">
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
            tdHighlight
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

      barChartRef: "calcSumBarChart",
      barChartXAxisName: "和值",
      barChartXAxisData: [],
      barChartYAxisName: "个数",
      barChartData: [],

      pieChartRef: "calcSumPieChart",
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
      let winningCalcSum = {}; // 号码-和值 字典
      let calcSumCounter = {}; // 和值-个数 字典
      for (let i = 0; i < 28; i++) calcSumCounter[i] = 0; // 初始化 和值-个数 字典
      for (let i = 0; i < this.lastest; i++) {
        let item = this.winningNumberList[i];
        let numAttr = 0;
        for (let char of item) numAttr += Number(char);
        calcSumCounter[numAttr]++;
        winningCalcSum[item] = numAttr;
      }

      /* 生成表格数据 */
      let calcSum = Object.keys(calcSumCounter);
      this.vuetifyTableData.headers = [];
      for (let i of calcSum) {
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
        for (let j of calcSum) item[j] = "";
        item[winningCalcSum[winningNo]] = winningNo;
        this.vuetifyTableData.items.push(item);
      }

      /* bar chart 数据 */
      this.barChartXAxisData = calcSum;
      this.barChartData = Object.values(calcSumCounter);

      /* pie chart 数据 */
      this.pieChartData = [];
      for (let i in calcSumCounter) {
        let item = {};
        item["name"] = i;
        item["value"] = calcSumCounter[i];
        this.pieChartData.push(item);
      }
      this.pieChartLegendData = calcSum;
    }
  }
};
</script>
