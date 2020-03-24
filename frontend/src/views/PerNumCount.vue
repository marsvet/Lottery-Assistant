<template>
  <v-container id="per-number-count" class="pt-0">
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
      <v-col cols="7">
        <v-text-field
          v-model="searchTable"
          append-icon="mdi-magnify"
          label="输入关键词搜索..."
          single-line
          hide-details
        ></v-text-field>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-card>
          <data-table
            :headers="vuetifyTableData.headers"
            :items="vuetifyTableData.items"
            :loading="tableLoading"
            :withBorder="false"
            :search="searchTable"
          ></data-table>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import DataTable from "../components/DataTable";

export default {
  components: {
    DataTable
  },
  data() {
    return {
      searchTable: "",
      tableLoading: true,
      lastest: -1, // 只显示最近 lastest 期。
      vuetifyTableData: {
        headers: [
          {
            text: "中奖号码",
            align: "center",
            value: "winningNo"
          },
          {
            text: "次数",
            align: "center",
            value: "count"
          }
        ],
        items: []
      }
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

      let winningCount = {}; // 号码-次数 字典
      for (let i = 0; i < this.lastest; i++) {
        let item = this.winningNumberList[i];
        if (winningCount[item]) winningCount[item]++;
        else winningCount[item] = 1;
      }

      this.vuetifyTableData.items = [];
      for (let item in winningCount) {
        this.vuetifyTableData.items.push({
          winningNo: item,
          count: winningCount[item]
        });
      }
      // 按中奖号码升序排序
      this.vuetifyTableData.items.sort((item1, item2) => {
        if (item1.winningNo > item2.winningNo) return 1;
        else if (item1.winningNo == item2.winningNo) return 0;
        else return -1;
      });
    }
  }
};
</script>
