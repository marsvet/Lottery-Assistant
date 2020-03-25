<template>
  <v-data-table
    :headers="headers"
    :items="items"
    :loading="loading"
    :dense="true"
    :search="search"
    :items-per-page="20"
    :hide-default-header="isMobile"
    :class="{
      'table-with-border': withBorder,
      'table-with-default-border': !withBorder
    }"
    :footer-props="{
      'items-per-page-options': [10, 20, 30, 40, 50, -1],
      'show-current-page': true,
      'show-first-last-page': true
    }"
  >
    <template v-slot:top>
      <v-row class="pl-5 pr-5">
        <v-col cols="6" sm="3" md="2" xl="1" class="pt-0">
          <v-text-field
            v-model="tdRowHeightTemp"
            prefix="行高："
            suffix="px"
            single-line
            hide-details
            class="text-field-center"
            @change="tdRowHeight = tdRowHeightTemp"
          ></v-text-field>
        </v-col>
        <v-col cols="6" sm="3" md="2" xl="1" class="pt-0">
          <v-text-field
            v-model="tdFontSizeTemp"
            prefix="字体："
            suffix="px"
            single-line
            hide-details
            class="text-field-center"
            @change="tdFontSize = tdFontSizeTemp"
          ></v-text-field>
        </v-col>
      </v-row>
    </template>
    <template v-slot:header="{ props }" v-if="isMobile">
      <tr>
        <td
          v-for="(item, index) in props.headers"
          :key="index"
          :class="{
            'text-start': item.align == 'start',
            'text-center': item.align == 'center',
            'text-end': item.align == 'end',
          }"
          style="border-bottom: thin solid rgba(0, 0, 0, 0.12); border-top: thin solid rgba(0, 0, 0, 0.12);"
        >{{ item.text }}</td>
      </tr>
    </template>
    <template v-slot:item="line">
      <tr>
        <td
          v-for="(header, index) in line.headers"
          :key="index"
          :style="tdStyle"
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
      tdRowHeightTemp: 20,
      tdFontSizeTemp: 15, // v-text-field v-model 属性的 .lazy 修饰符不起作用，这两个 temp 数据只是为了手动实现 .lazy 的功能
      tdRowHeight: 20,
      tdFontSize: 15
    };
  },
  computed: {
    tdStyle() {
      return {
        height: this.tdRowHeight + "px",
        "line-height": this.tdRowHeight + "px",
        "font-size": this.tdFontSize + "px"
      };
    },
    isMobile() {
      // 当不是手机时，使用 vuetify 默认的表格头；当是手机时，使用自定义的表格头
      // vuetify 默认的表格头在手机中显示时，会显示成竖着的，而这个项目不需要这个功能，但又无法让它显示成横的，所以出此下策，等待 vuetify 提供自定义表头的功能以后再说。
      // 自定义的表格头无法使用一些功能如排序，先凑活着用吧
      return this.$vuetify.breakpoint.xs;
    }
  }
};
</script>

<style scoped>
.tdHighlight {
  background-color: yellow;
}
</style>
