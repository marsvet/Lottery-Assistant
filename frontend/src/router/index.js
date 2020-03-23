import Vue from "vue";
import VueRouter from "vue-router";

Vue.use(VueRouter);

const AllData = () => import("../views/AllData");
const PerNumCount = () => import("../views/PerNumCount");
const CountStatistics = () => import("../views/CountStatistics");
const OddEven = () => import("../views/OddEven");
const BigSmall = () => import("../views/BigSmall");
const YinYang = () => import("../views/YinYang");
const PrimeComposite = () => import("../views/PrimeComposite");
const CalcSum = () => import("../views/CalcSum");
const Calc012 = () => import("../views/Calc012");
const CalcSpan = () => import("../views/CalcSpan");

const routes = [
  {
    path: "/",
    component: AllData,
    meta: {
      title: "数据总览 - 彩票助手"
    }
  },
  {
    path: "/per_number_count",
    component: PerNumCount,
    meta: {
      title: "号码出现次数 - 彩票助手"
    }
  },
  {
    path: "/count_statistics",
    component: CountStatistics,
    meta: {
      title: "次数统计 - 彩票助手"
    }
  },
  {
    path: "/odd_even",
    component: OddEven,
    meta: {
      title: "奇偶 - 彩票助手"
    }
  },
  {
    path: "/big_small",
    component: BigSmall,
    meta: {
      title: "大小 - 彩票助手"
    }
  },
  {
    path: "/yin_yang",
    component: YinYang,
    meta: {
      title: "阴阳 - 彩票助手"
    }
  },
  {
    path: "/prime_composite",
    component: PrimeComposite,
    meta: {
      title: "质和 - 彩票助手"
    }
  },
  {
    path: "/calc_sum",
    component: CalcSum,
    meta: {
      title: "和值 - 彩票助手"
    }
  },
  {
    path: "/calc_012",
    component: Calc012,
    meta: {
      title: "012路 - 彩票助手"
    }
  },
  {
    path: "/calc_span",
    component: CalcSpan,
    meta: {
      title: "跨度 - 彩票助手"
    }
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

export default router;
