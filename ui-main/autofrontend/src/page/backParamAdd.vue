<template>
  <div>
    <head-top></head-top>
    <el-row style="margin-top: 50px; algin: center">
      <el-col :span="15" :offset="4">
        <header class="form_header">参数配置（新增）</header>
        <br />
        <template>
          <el-form
            :inline="true"
            :model="resourceForm"
            :rules="resourceRules"
            ref="resourceForm"
            size="mini"
            label-position="right"
            label-width="98px"
          >
            <div class="form param_form">
              <el-form-item label="用例名称" prop="casename" :required="true">
                <el-input
                  v-model="resourceForm.casename"
                  placeholder="请输入中文（全局唯一）"
                  clearable
                  style="width: 258px;"
                ></el-input>
              </el-form-item>
              <el-form-item label="用例方法" :required="true" size="mini" prop="caseFunc">
                <el-input
                  v-model="resourceForm.caseFunc"
                  placeholder="请输入英文（全局唯一，创建后不可更改只能删除）"
                  clearable
                  @blur="showPresentStep()"
                  style="width: 258px;"
                ></el-input>
              </el-form-item>
              <el-form-item label="用例分组" :required="true" prop="caseType" size="mini">
                <el-select
                  v-model="resourceForm.caseType"
                  clearable
                  filterable
                  size="mini"
                  :allow-create="false"
                  style="width: 258px;"
                >
                  <el-option
                    v-for="item in return_list"
                    :key="item"
                    :label="item"
                    :value="item"
                  ></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="归属环境" :required="true" prop="caseEnv" size="mini">
                <el-select
                  v-model="resourceForm.caseEnv"
                  clearable
                  filterable
                  size="mini"
                  :allow-create="false"
                  style="width: 258px;"
                >
                  <el-option
                    v-for="item in return_env_list"
                    :key="item.Env_name"
                    :label="item.desc"
                    :value="item.Env_name"
                  ></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="备注" :required="false" size="mini" prop="caseRemark">
                <el-input
                  v-model="resourceForm.caseRemark"
                  placeholder="请输入"
                  clearable
                  style="width: 258px;"
                ></el-input>
              </el-form-item>
            </div>
            <div class="form param_form">
              <el-form-item label="动作方法" prop="eleAction" :required="true">
                <el-select
                  v-model="resourceForm.eleAction"
                  clearable
                  filterable
                  size="mini"
                  no-data-text
                  @visible-change="collectElementAction()"
                  @change="valueRequired(value='action')"
                  class="argvForm"
                >
                  <el-option v-for="item in resourceForm.methodList" :key="item" :value="item"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="动作描述" :required="true" size="mini" prop="actionDesc">
                <el-input
                  v-model="resourceForm.actionDesc"
                  placeholder="请输入"
                  clearable
                  style="width: 258px;"
                ></el-input>
              </el-form-item>
              <el-form-item label="步骤顺序" :required="true" size="mini" prop="stepSequence">
                <el-select
                  clearable
                  style="width: 258px;"
                  v-model="resourceForm.stepSequence"
                  size="mini"
                  filterable
                  :placeholder="stepMessage"
                  @visible-change="showPresentStep()"
                >
                  <el-option
                    v-for="(item) in 100"
                    :key="item"
                    :label="`第${item}步`"
                    :value="item"
                  ></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="定位方式" :required="false" size="mini" prop="locateType">
                <el-select
                  v-model="resourceForm.locateType"
                  clearable
                  style="width: 258px;"
                  size="mini"
                  @change="valueRequired()"
                >
                  <el-option value="xpath"></el-option>
                  <el-option value="id"></el-option>
                  <el-option value="name"></el-option>
                  <el-option value="class name"></el-option>
                  <el-option value="tag name"></el-option>
                  <el-option value="link text"></el-option>
                  <el-option value="partial link text"></el-option>
                  <el-option value="css selector"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="定位元素值" :required="eleRequired" size="mini" prop="locateValue">
                <el-input
                  v-model="resourceForm.locateValue"
                  placeholder="请输入"
                  clearable
                  style="width: 258px;"
                ></el-input>
              </el-form-item>
              <el-form-item label="动作参数" :required="actionRequired" size="mini" prop="actionValue">
                <el-input
                  v-model="resourceForm.actionValue"
                  placeholder="请输入"
                  clearable
                  style="width: 258px;"
                ></el-input>
              </el-form-item>
              <el-form-item label="动作断言值" :required="false" size="mini" prop="assertValue">
                <el-input
                  v-model="resourceForm.assertValue"
                  placeholder="请输入"
                  clearable
                  style="width: 258px;"
                ></el-input>
              </el-form-item>
              <el-form-item
                size="mini"
                v-for="(newArgv, index) in resourceForm.argvs"
                :label="'扩展参数' + (index+1) + ': ' + newArgv.name"
                :key="newArgv.name"
                :prop="'argvs.'+ index + '.value'"
                :rules="{
      required: true, message: '参数值不能为空', trigger: 'blur'
    }"
              >
                <el-input
                  v-model="newArgv.value"
                  clearable
                  filterable
                  style="width: 258px;"
                  placeholder="请输入"
                ></el-input>
              </el-form-item>
              <el-form-item label="备注" :required="false" size="mini" prop="remark">
                <el-input
                  v-model="resourceForm.remark"
                  placeholder="请输入"
                  clearable
                  style="width: 258px;"
                ></el-input>
              </el-form-item>
              <br />
            </div>
            <el-form-item style="margin-left: 366px">
              <el-tooltip class="item" effect="dark" placement="top">
                <div slot="content">
                  提交数据
                  <br />
                </div>
                <el-button
                  type="primary"
                  @click="onSubmmitAddArgvs()"
                  round
                  icon="el-icon-circle-plus"
                >新增</el-button>
              </el-tooltip>
              <el-tooltip class="item" effect="dark" placement="top">
                <div slot="content">
                  提交数据，
                  <br />环境*省份*用例名
                </div>
                <el-button type="danger" round icon="el-icon-edit" @click="resetForm()">重置</el-button>
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
import { showLoading, hideLoading } from '@/config/common'
import {
  backendManageGetCaseArgvs,
  backendManageAddCaseArgvs,
  backendManageAddStepArgvs,
  backendManageQueryPresentStep,
  backendManageQuerygroup,
  backendManageQueryenv
} from '@/api/getData'
const stepOrder = [
  { desc: '第一步', order: 1 },
  { desc: '第二步', order: 2 },
  { desc: '第三步', order: 3 },
  { desc: '第四步', order: 4 },
  { desc: '第五步', order: 5 },
  { desc: '第六步', order: 6 },
  { desc: '第七步', order: 7 },
  { desc: '第八步', order: 8 },
  { desc: '第九步', order: 9 },
  { desc: '第十步', order: 10 },
  { desc: '第十一步', order: 11 },
  { desc: '第十二步', order: 12 },
  { desc: '第十三步', order: 13 },
  { desc: '第十四步', order: 14 },
  { desc: '第十五步', order: 15 },
  { desc: '第十六步', order: 16 },
  { desc: '第十七步', order: 17 },
  { desc: '第十八步', order: 18 },
  { desc: '第十九步', order: 19 },
  { desc: '第二十步', order: 20 }
]
export default {
  data () {
    return {
      return_env_list: [],
      return_list: [],
      stepOrder,
      stepMessage: '',
      presentStepSeq: 0,
      eleRequired: false,
      actionRequired: false,
      argvsPost: [],
      resourceRules: {
        casename: [
          { required: true, message: '请输入用例名', trigger: 'blur' }
        ],
        caseFunc: [
          { required: true, message: '请输入用例方法名', trigger: 'blur' }
        ],
        caseType: [
          { required: true, message: '请输入用例分组', trigger: 'blur' }
        ],
        caseEnv: [
          { required: true, message: '请输入用例归属环境', trigger: 'blur' }
        ],
        eleAction: [
          { required: true, message: '请选择操作方法', trigger: 'blur' }
        ],
        actionDesc: [
          { required: true, message: '请输入动作描述', trigger: 'blur' }
        ],
        locateValue: [{ message: '请输入元素定位值', trigger: 'blur' }],
        stepSequence: [
          { required: true, message: '请选择步骤', trigger: 'blur' }
        ]
      },
      resourceForm: {
        caseFunc: '',
        caseType: '',
        caseEnv: '',
        caseRemark: '',
        casename: '',
        actionDesc: '',
        locateType: '',
        stepSequence: '',
        eleAction: '',
        locateValue: '',
        actionValue: '',
        assertValue: '',
        remark: '',
        methodList: [],
        argvs: []
      }
    }
  },
  components: {
    headTop
  },
  created: function () {
    this.getGroupName()
    this.getEnvName()
  },
  mounted () {},
  methods: {
    async getGroupName () {
      showLoading()
      try {
        const resp = await backendManageQuerygroup()
        if (resp.code === 0) {
          this.return_list = resp.data
          // this.$message({
          //   type: 'success',
          //   message:
          //     '查询成功, 共计 ' + this.return_list.length + ' 条分组...'
          // })
        }
      } catch (err) {
        this.$message.error(err.message)
      } finally {
        hideLoading()
      }
    },
    async getEnvName () {
      showLoading()
      try {
        const resp = await backendManageQueryenv({ 'IfAll': true })
        if (resp.code === 0) {
          this.return_env_list = resp.data
          // this.$message({
          //   type: 'success',
          //   message:
          //     '查询成功, 共计 ' + this.return_env_list.length + ' 个环境...'
          // })
        }
      } catch (err) {
        this.$message.error(err.message)
      } finally {
        hideLoading()
      }
    },
    resetForm () {
      this.$refs.resourceForm.resetFields()
      this.$message({
        type: 'success',
        message: '已清除'
      })
    },
    valueRequired (value = 'element') {
      if (value === 'element') {
        this.eleRequired = !!this.resourceForm.locateType
      } else {
        this.actionRequired =
          this.resourceForm.eleAction === 'input'
      }
    },
    async showPresentStep () {
      try {
        const resp = await backendManageQueryPresentStep({
          case_func: this.resourceForm.caseFunc
        })
        if (resp.ResCode === 0) {
          this.presentStepSeq = resp.step_count
          if (resp.step_count) {
            this.stepMessage = `当前用例已经存在【${resp.step_count}】步配置信息`
          } else {
            this.stepMessage = '请选择步骤'
          }
        }
      } catch (err) {
        this.$message.error(err.message)
      }
    },
    async onSubmmitAddArgvs (form = 'resourceForm') {
      this.$refs[form].validate(async valid => {
        try {
          const argvsObject = this.argvsPost.reduce((p, c, i) => {
            p[c] = this.resourceForm.argvs[i].value
            return p
          }, {})
          if (valid) {
            const param = {
              casename: this.resourceForm.casename,
              case_func: this.resourceForm.caseFunc,
              case_type: this.resourceForm.caseType,
              case_env: this.resourceForm.caseEnv,
              caseRemark: this.resourceForm.caseRemark,
              action_desc: this.resourceForm.actionDesc,
              ele_action: this.resourceForm.eleAction,
              locate_type: this.resourceForm.locateType,
              step_seq: this.resourceForm.stepSequence,
              locate_value: this.resourceForm.locateValue,
              action_value: this.resourceForm.actionValue,
              assert_value: this.resourceForm.assertValue,
              remark: this.resourceForm.remark,
              argvs: argvsObject
            }
            if (this.presentStepSeq + 1 < this.resourceForm.stepSequence) {
              this.$notify.error({
                message: `最大添加步骤应为【${this.presentStepSeq + 1}】`,
                center: true,
                showClose: true,
                duration: 0
              })
              return
            }
            const resp = await backendManageAddCaseArgvs(param)
            if (resp.ResCode === 0) {
              this.$notify.success({
                showClose: true,
                message: '写入用例成功！',
                center: true
              })
              const resp = await backendManageAddStepArgvs(param)
              if (resp.ResCode === 0) {
                this.$notify.success({
                  showClose: true,
                  message: '写入用例步骤成功！',
                  center: true
                })
              } else {
                this.$notify.error({
                  message: resp.ErrMsg || '操作失败！',
                  center: true,
                  showClose: true,
                  duration: 0
                })
              }
            } else {
              this.$notify.error({
                message: resp.ErrMsg || '写入用例失败！',
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
    },
    async collectElementAction () {
      try {
        const resp = await backendManageGetCaseArgvs({
          funcname: 'collectElementAction'
        })
        if (resp.ResCode === 0) {
          this.resourceForm.methodList = []
          this.resourceForm.methodList = resp.operation_method
          this.generateArgvsList()
        } else {
          this.$message({
            type: 'error',
            message: resp.ErrMsg,
            center: true
          })
        }
      } catch (err) {
        this.$message.error(err.message)
      }
    },
    async generateArgvsList () {
      this.resourceForm.argvs = []
      try {
        const resp = await backendManageGetCaseArgvs({
          funcname: 'generatorArgvsList'
        })
        if (resp.ResCode === 0) {
          this.argvsPost = []
          const extend_argvs = resp.argvs[this.resourceForm.eleAction] || []
          if (extend_argvs.length !== 0) {
            this.argvsPost = extend_argvs
            this.argvsPost.forEach((item, index) => {
              let data = {}
              data.name = item
              this.resourceForm.argvs.push(data)
            })
          }
        } else {
          this.$message({
            type: 'error',
            message: resp.ErrMsg,
            center: true
          })
        }
      } catch (err) {
        this.$message.error(err.message)
      }
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
