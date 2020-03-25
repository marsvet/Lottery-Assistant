<template>
  <v-data-table
    :headers="headers"
    :items="items"
    :loading="loading"
    :dense="denseTable"
    :search="search"
    :items-per-page="20"
    :class="{ 'table-with-border': withBorder, 'table-with-default-border': !withBorder }"
    :footer-props="{
      'items-per-page-options': [10, 20, 30, 40, 50, -1],
      'show-current-page': true,
      'show-first-last-page': true
    }"
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
    <template v-slot:item="line">
      <tr>
        <td
          v-for="(header, index) in line.headers"
          :key="index"
          :class="{
            'text-start': header.align == 'start',
            'text-center': header.align == 'center',
            'text-end': header.align == 'end',
            'tdHighlight': tdHighlight && line.item[header.value]
          }"
        >{{ line.item[header.value] }}</td>
      </tr>
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
    },
    tdHighlight: {
      type: Boolean,
      default: false
    } // 当该 prop 为 true 并且 td 内容不为空时，td 被高亮
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

<style scoped>
.tdHighlight {
  background-color: yellow;
}
</style>
