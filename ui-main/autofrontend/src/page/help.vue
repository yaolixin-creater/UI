<template>
  <div>
    <template>
      <div>
        <head-top></head-top>
        <div class="div_cls">
          <h2 style="color:dimgrey;">&nbsp;&nbsp;常用动作方法说明:</h2>
          <div>
            <el-collapse v-model="activeNames" @change="handleChange" class="title">
              <el-collapse-item title="assert_find_element" name="1">
                <h4>&nbsp;&nbsp;用于断言某个页面元素是否存在</h4>
                <h4>&nbsp;&nbsp;需要填写的对象：定位方式，定位元素值</h4>
              </el-collapse-item>
              <el-collapse-item title="assert_find_text" name="2">
                <h4>&nbsp;&nbsp;用于断言某个页面元素是否等于某个值</h4>
                <h4>&nbsp;&nbsp;需要填写的对象：定位方式，定位元素值，动作断言值</h4>
              </el-collapse-item>
              <el-collapse-item title="assert_wait_response" name="3">
                <h4>&nbsp;&nbsp;用于断言是否发起某个请求</h4>
                <h4>&nbsp;&nbsp;需要填写的对象：定位方式，定位元素值，动作断言值</h4>
                <h4>&nbsp;&nbsp;动作断言值填url中域名之后的值</h4>
              </el-collapse-item>
              <el-collapse-item title="banckend_menu_scroll" name="13">
                <h4>&nbsp;&nbsp;后端管理员视图下滑</h4>
                <h4>&nbsp;&nbsp;需要填写的对象：动作参数按需填写</h4>
              </el-collapse-item>
              <el-collapse-item title="click" name="4">
                <h4>&nbsp;&nbsp;用于点击某个元素</h4>
                <h4>&nbsp;&nbsp;需要填写的对象：定位方式，定位元素值</h4>
              </el-collapse-item>
              <el-collapse-item title="compulsively_wait" name="5">
                <h4>&nbsp;&nbsp;强制等待一段时间</h4>
                <h4>&nbsp;&nbsp;需要填写的对象：动作参数</h4>
                <h4>&nbsp;&nbsp;填入2,代表等待2s</h4>
              </el-collapse-item>
              <el-collapse-item title="get_url" name="6">
                <h4>&nbsp;&nbsp;请求某个地址</h4>
                <h4>&nbsp;&nbsp;需要填写的对象：动作参数</h4>
              </el-collapse-item>
              <el-collapse-item title="input" name="7">
                <h4>&nbsp;&nbsp;用于文本框输入某个文本值</h4>
                <h4>&nbsp;&nbsp;需要填写的对象：定位方式，定位元素，动作参数</h4>
                <h4>&nbsp;&nbsp;动作参数是输入的文本内容，如果输入{random_str}，则填入随机字符串</h4>
              </el-collapse-item>
              <el-collapse-item title="open_new_window" name="8">
                <h4>&nbsp;&nbsp;句柄跳到最新打开的窗口</h4>
                <h4>&nbsp;&nbsp;需要填写的对象：不需要</h4>
              </el-collapse-item>
              <el-collapse-item title="refresh_get_url" name="12">
                <h4>&nbsp;&nbsp;打开新的地址，和选中的环境绑定，域名处填入{host}，用于实现通用用例的独立性</h4>
                <h4>&nbsp;&nbsp;需要填写的对象：动作参数</h4>
                <h4>&nbsp;&nbsp;需要注意的是，域名处用{host}替换</h4>
              </el-collapse-item>
<!--              <el-collapse-item title="scroll_window_bottom" name="9">-->
<!--                <h4>&nbsp;&nbsp;滑动到窗口底部</h4>-->
<!--                <h4>&nbsp;&nbsp;需要填写的对象：不需要</h4>-->
<!--              </el-collapse-item>-->
<!--              <el-collapse-item title="scroll_window_top" name="10">-->
<!--                <h4>&nbsp;&nbsp;滑动到窗口顶部</h4>-->
<!--                <h4>&nbsp;&nbsp;需要填写的对象：不需要</h4>-->
<!--              </el-collapse-item>-->
              <el-collapse-item title="switch_to_childframe" name="11">
                <h4>&nbsp;&nbsp;切换到新的iframe框，默认切入到第一个，可以填指定的位置</h4>
                <h4>&nbsp;&nbsp;需要填写的对象：动作参数按需填写</h4>
              </el-collapse-item>
            </el-collapse>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import headTop from '@/components/headTop'
export default {
  data () {
    return {
      src: ''
    }
  },
  components: {
    headTop
  }
}
</script>

<style lang="less" scoped>
@import "../style/mixin";

.div_cls {
  max-height: 100%; // 高度
  width: 65%; // 宽度
}
.title{
  margin-left:30px // 空格距离
}
</style>
