<template>
  <v-container id="all-data" class="pt-0">
    <v-row>
      <v-col cols="0" sm="5"></v-col>
      <v-col cols="12" sm="7">
        <v-text-field
          v-model="search"
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
          <v-data-table
            :headers="vuetifyTableData.headers"
            :items="vuetifyTableData.items"
            :items-per-page="10"
            :search="search"
            :loading="loading"
            :dense="denseTable"
            class="table-with-default-border"
          >
            <template v-slot:top>
              <v-btn
                class="mt-4 mb-4 ml-3 ml-sm-10"
                outlined
                rounded
                color="primary"
                @click="denseTable = !denseTable"
              >{{ btnText }}</v-btn>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      search: "",
      loading: true,
      denseTable: false,
      vuetifyTableData: {
        headers: [
          {
            text: "期号",
            align: "center",
            sortable: false,
            value: "phaseNo"
          },
          {
            text: "开奖日期",
            align: "center",
            sortable: false,
            value: "date"
          },
          {
            text: "中奖号码_百位",
            align: "center",
            sortable: false,
            value: "hundreds"
          },
          {
            text: "中奖号码_十位",
            align: "center",
            sortable: false,
            value: "tens"
          },
          {
            text: "中奖号码_个位",
            align: "center",
            sortable: false,
            value: "singles"
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
    btnText() {
      return this.denseTable == true ? "关闭密集模式" : "开启密集模式";
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
      this.loading = false;
      let data = JSON.parse(JSON.stringify(this.allData)); // 复制

      for (let row of data) {
        let item = {};
        item["phaseNo"] = row[0];
        item["date"] = row[1];
        item["hundreds"] = row[2];
        item["tens"] = row[3];
        item["singles"] = row[4];
        this.vuetifyTableData.items.push(item);
      }
    }
  }
};
</script>
