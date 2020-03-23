import Vue from "vue";
import "./plugins/axios";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import vuetify from "./plugins/vuetify";
import VueWechatTitle from "vue-wechat-title";
import echarts from "echarts"; // 引入 echarts

Vue.prototype.$echarts = echarts;
Vue.use(VueWechatTitle);
Vue.config.productionTip = false;

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount("#app");
