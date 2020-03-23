<template>
  <div class="bar-chart-container" :ref="chartRef" style="height: 400px;"></div>
</template>

<script>
export default {
  props: {
    chartRef: String,

    xAxisName: String,
    xAxisData: Array,
    yAxisName: String,
    data: Array
  },
  data() {
    return { myChart: null };
  },
  computed: {
    option() {
      return {
        xAxis: {
          name: this.xAxisName,
          type: "category",
          data: this.xAxisData,
          axisTick: {
            alignWithLabel: true // 坐标轴刻度与柱子对齐
          }
        },
        yAxis: {
          name: this.yAxisName,
          type: "value"
        },
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "shadow"
          }
        },
        series: [
          {
            data: this.data,
            type: "bar",
            label: {
              show: true,
              position: "top",
              fontWeight: "bold"
            }
          }
        ]
      };
    }
  },
  watch: {
    data() {
      this.myChart.setOption(this.option);
    }
  },
  mounted() {
    this.myChart = this.$echarts.init(this.$refs[this.chartRef]);
    this.myChart.setOption(this.option);
  }
};
</script>
