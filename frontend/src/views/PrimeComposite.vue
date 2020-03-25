<template>
  <v-container id="prime-composite" class="pt-0">
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

      barChartRef: "primeCompositeBarChart",
      barChartXAxisName: "质合",
      barChartXAxisData: [],
      barChartYAxisName: "个数",
      barChartData: [],

      pieChartRef: "primeCompositePieChart",
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
    isPrimeNumber(num) {
      //判断 num 是否为质数。这里把 0 看做合数，1 看做质数
      if (num == 0) return false;
      if (num == 1) return true;
      for (let i = 2; i < num; i++) if (num % i == 0) return false;
      return true;
    },
    setData() {
      this.tableLoading = false;
      this.lastestChanged();
    },
    lastestChanged() {
      if (this.lastest < 0 || this.lastest > this.allData.length)
        this.lastest = this.allData.length;

      /* 准备数据 */
      let winningPrimeComposite = {}; // 号码-质合 字典
      let primeCompositeCounter = {
        质质质: 0,
        质质合: 0,
        质合质: 0,
        质合合: 0,
        合质质: 0,
        合质合: 0,
        合合质: 0,
        合合合: 0
      }; // 质合-个数 字典
      for (let i = 0; i < this.lastest; i++) {
        let item = this.winningNumberList[i];
        let numAttr = "";
        for (let char of item)
          numAttr += this.isPrimeNumber(char) ? "质" : "合";
        primeCompositeCounter[numAttr]++;
        winningPrimeComposite[item] = numAttr;
      }

      /* 生成表格数据 */
      let primeComposite = Object.keys(primeCompositeCounter);
      this.vuetifyTableData.headers = [];
      for (let i of primeComposite) {
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
        for (let j of primeComposite) item[j] = "";
        item[winningPrimeComposite[winningNo]] = winningNo;
        this.vuetifyTableData.items.push(item);
      }

      /* bar chart 数据 */
      this.barChartXAxisData = primeComposite;
      this.barChartData = Object.values(primeCompositeCounter);

      /* pie chart 数据 */
      this.pieChartData = [];
      for (let i in primeCompositeCounter) {
        let item = {};
        item["name"] = i;
        item["value"] = primeCompositeCounter[i];
        this.pieChartData.push(item);
      }
      this.pieChartLegendData = primeComposite;
    }
  }
};
</script>
