<template>
  <div>
    <head-top></head-top>
    <el-row style="margin-top: 50px; algin: center">
      <el-col :span="15" :offset="4">
        <header class="form_header">复用步骤修改</header>
        <br />
        <template>
          <el-form
            :inline="true"
            :model="resourceForm"
            :rules="resourceRules"
            ref="resourceForm"
            size="mini"
            label-position="right"
            label-width="108px"
          >
              <el-form-item label="动作描述" :required="true" size="mini" prop="actionDesc">
                <el-input
                  v-model="resourceForm.actionDesc"
                  placeholder="请输入"
                  clearable
                  style="width: 108px;"
                ></el-input>
              </el-form-item>
              <el-form-item label="元素定位值" :required="true" size="mini" prop="locateValue">
                <el-input
                  v-model="resourceForm.locateValue"
                  placeholder="请输入"
                  clearable
                  style="width: 108px;"
                ></el-input>
              </el-form-item>
            <el-form-item label="定位元素值new" :required="true" size="mini" prop="locateValuenew">
                <el-input
                  v-model="resourceForm.locateValuenew"
                  placeholder="请输入"
                  clearable
                  style="width: 108px;"
                ></el-input>
              </el-form-item>
              <br />
            <el-form-item style="margin-left: 288px">
              <el-tooltip class="item" effect="dark" placement="top">
                <div slot="content">
                  修改，
                  <br />全局操作
                </div>
                <el-button
                  type="primary"
                  @click="onSubmmitAddArgvs()"
                  round
                  icon="el-icon-edit"
                >修改</el-button>
              </el-tooltip>
              <el-tooltip class="item" effect="dark" placement="top">
                <div slot="content">
                  清空输入框
                </div>
                <el-button type="danger" round icon="el-icon-view" @click="resetForm()">重置</el-button>
              </el-tooltip>
            </el-form-item>
          </el-form>
        </template>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import headTop from '@/components/headTop'
import {
  modifysteps
} from '@/api/getData'
export default {
  data () {
    return {
      resourceRules: {
        actionDesc: [
          { required: true, message: '请输入动作描述', trigger: 'blur' }
        ],
        locateValue: [{ message: '请输入元素定位值', trigger: 'blur' }],
        locateValuenew: [
          { required: true, message: '请输入新的元素定位值', trigger: 'blur' }
        ]
      },
      resourceForm: {
        locateValuenew: '',
        locateValue: '',
        actionDesc: ''
      }
    }
  },
  components: {
    headTop
  },
  methods: {
    resetForm () {
      this.$refs.resourceForm.resetFields()
      this.$message({
        showClose: true,
        type: 'success',
        message: '已清除'
      })
    },
    async onSubmmitAddArgvs (form = 'resourceForm') {
      this.$refs[form].validate(async valid => {
        try {
          if (valid) {
            const param = {
              action_desc: this.resourceForm.actionDesc,
              locate_value: this.resourceForm.locateValue,
              locate_value_new: this.resourceForm.locateValuenew
            }
            const resp = await modifysteps(param)
            if (resp.ResCode === 0) {
              if (resp.lens === 0) {
                this.$notify.error({
                  message: '根据条件没找到步骤',
                  center: true
                })
              } else {
                this.$notify.success({
                  showClose: true,
                  message: '修改用例成功！',
                  center: true
                })
              }
            } else {
              this.$notify.error({
                message: resp.ErrMsg || '修改用例失败！',
                center: true,
                showClose: true,
                duration: 0
              })
            }
          } else {
            this.$notify.error({
              title: 'ERROR',
              message: '亲，必填项不能为空哟',
              offset: 288
            })
          }
        } catch (err) {
          this.$message.error(err.message)
        }
      })
    }
  }
}
</script>

<style lang="less">
@import "../style/mixin";
.form {
  min-width: 100%;
  margin-bottom: 20px;
  &:hover {
    box-shadow: 0 0 8px 0 rgba(232, 237, 250, 0.6),
      0 2px 4px 0 rgba(232, 237, 250, 0.5);
    border-radius: 10px;
    transition: all 400ms;
  }
}
.param_form {
  border: 1px solid #eaeefb;
  padding: 2% 2% 1% 8%;
}
.form_header {
  text-align: center;
  margin-bottom: 10px;
}

.argvForm {
  width: 258px;
}
</style>
