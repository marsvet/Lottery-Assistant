import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    allData: [],
    winningNumberList: []
  },
  mutations: {
    ["setAllData"](state, data) {
      if (data.success == true) {
        state.allData = data.data;
        state.allData.reverse();

        // set winningNumberList
        state.winningNumberList = [];
        for (let item of state.allData) {
          let number = String(item[2]) + item[3] + item[4];
          state.winningNumberList.push(number);
        }
      }
    }
  }
});
