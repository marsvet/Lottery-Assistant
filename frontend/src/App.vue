<template>
  <v-app id="app">
    <menu-bar></menu-bar>
    <v-content>
      <keep-alive>
        <router-view v-wechat-title="$route.meta.title"></router-view>
      </keep-alive>
    </v-content>
  </v-app>
</template>

<script>
import MenuBar from "./components/MenuBar";
import { getAllData } from "./network/index.js";

export default {
  components: {
    MenuBar
  },
  created() {
    getAllData().then(rsp => {
      this.$store.commit("setAllData", rsp.data);
    });
  }
};
</script>

<style>
@import "./assets/css/base.css";

.text-field-center input {
  text-align: center;
}

.table-with-border td,
.table-with-border th {
  border-left: thin solid rgba(0, 0, 0, 0.12);
}

.table-with-border td:first-child,
.table-with-border th:first-child {
  border-left: none;
}

.table-with-border th,
.table-with-default-border th {
  border-top: thin solid rgba(0, 0, 0, 0.12);
}
</style>
