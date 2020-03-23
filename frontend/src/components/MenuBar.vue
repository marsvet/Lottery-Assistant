<template>
  <div>
    <v-navigation-drawer id="menu-bar" v-model="drawer" :clipped="$vuetify.breakpoint.lgAndUp" app>
      <v-list>
        <v-list-item v-for="(page,index) in pages" :key="index" :to="page.route">
          <v-list-item-action>
            <!-- <v-icon>{{ page.icon }}</v-icon> -->
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>{{ page.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar :clipped-left="$vuetify.breakpoint.lgAndUp" app color="blue darken-3" dark>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <v-toolbar-title style="width: 300px" class="ml-0 pl-4">
        <span class="hidden-sm-and-down">彩票助手</span>
      </v-toolbar-title>
    </v-app-bar>
  </div>
</template>

<script>
export default {
  data() {
    return {
      drawer: true,
      pages: [
        {
          route: "/",
          title: "数据总览"
          // icon: "mdi-home"
        },
        {
          route: "/per_number_count",
          title: "号码出现次数"
          // icon: "mdi-home"
        },
        {
          route: "/count_statistics",
          title: "次数统计"
          // icon: "mdi-home"
        },
        {
          route: "/odd_even",
          title: "奇偶"
          // icon: "mdi-home"
        },
        {
          route: "/big_small",
          title: "大小"
          // icon: "mdi-home"
        },
        {
          route: "/yin_yang",
          title: "阴阳"
          // icon: "mdi-home"
        },
        {
          route: "/prime_composite",
          title: "质和"
          // icon: "mdi-home"
        },
        {
          route: "/calc_sum",
          title: "和值"
          // icon: "mdi-home"
        },
        {
          route: "/calc_012",
          title: "012路"
          // icon: "mdi-home"
        },
        {
          route: "/calc_span",
          title: "跨度"
          // icon: "mdi-home"
        }
      ]
    };
  }
};
</script>
