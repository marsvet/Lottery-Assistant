<template>
  <v-data-table
    :headers="headers"
    :items="items"
    :loading="loading"
    :dense="denseTable"
    :search="search"
    :items-per-page="20"
    :footer-props="{
      'items-per-page-options': [10, 20, 30, 40, 50, -1],
      'show-current-page': true,
      'show-first-last-page': true
    }"
    :class="{'table-with-border': withBorder, 'table-with-default-border': !withBorder }"
  >
    <template v-slot:top>
      <v-btn
        class="mt-4 mb-4 ml-3 ml-sm-10"
        outlined
        rounded
        small
        color="primary"
        @click="denseTable = !denseTable"
      >{{ btnText }}</v-btn>
    </template>
  </v-data-table>
</template>

<script>
export default {
  props: {
    headers: Array,
    items: Array,
    loading: Boolean,
    withBorder: Boolean,
    search: {
      type: String,
      default: ""
    }
  },
  data() {
    return {
      denseTable: true
    };
  },
  computed: {
    btnText() {
      return this.denseTable == true ? "关闭密集模式" : "开启密集模式";
    }
  }
};
</script>
