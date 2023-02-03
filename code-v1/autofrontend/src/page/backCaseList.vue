<template>
  <div>
    <head-top></head-top>
    <div style="margin-left: 20px; margin-top: 20px; margin-right: 0; font-size: 14px">
      <el-form
        :inline="true"
        :model="caseForm"
        :rules="caseRules"
        ref="caseForm"
        class="form-auto"
        label-width="80px"
        size="mini"
      >
        <el-form-item label="用例分组" :required="false" prop="group">
          <el-select
            v-model="caseForm.group"
            clearable
            filterable
            multiple
            size="mini"
            :allow-create="false"
            @change="onQueryGroupCase()"
          >
            <el-option
                v-for="item in return_list"
                :key="item"
                :label="item"
                :value="item"
              ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="归属环境" :required="true" prop="env">
          <el-select
            v-model="caseForm.env"
            clearable
            filterable
            size="mini"
            @change="onQueryGroupCase()"
          >
            <el-option
              v-for="item in return_env_list"
              :key="item.Env_name"
              :label="item.desc"
              :value="item.Env_name"
            ></el-option>
          </el-select>
        </el-form-item>
<!--        <el-form-item label="并发执行" prop="perform_num">-->
<!--          <el-select-->
<!--            v-model="caseForm.perform_num"-->
<!--            clearable-->
<!--            filterable-->
<!--            size="mini"-->
<!--            style="width: 60px"-->
<!--          >-->
<!--            <el-option-->
<!--              v-for="item in 6"-->
<!--              :key="item"-->
<!--              :label="item"-->
<!--              :value="item"-->
<!--            ></el-option>-->
<!--          </el-select>-->
<!--        </el-form-item>-->
        <!-- <el-form-item label="测试描述" :required="false" prop="description">
          <el-input v-model="caseForm.description" placeholder="请输入" clearable size="mini"></el-input> -->
        <!-- </el-form-item> -->
        <el-form-item>
          <el-tooltip
            class="item"
            effect="dark"
            placement="top"
            :hide-after="5000"
            :enterable="false"
          >
            <div slot="content">
              如果您未勾选任何用例,
              <br />默认将执行全部用例;
              <br />点击之前请先选择必选数据项
            </div>
            <el-button
              type="primary"
              round
              @click="onTest('caseForm')"
              plain
              icon="el-icon-video-camera-solid"
              :loading="loadingValue"
              :disabled="clickAble"
              size="mini"
            >执行</el-button>
          </el-tooltip>
        </el-form-item>
        <el-form-item>
          <el-button
            type="danger"
            @click="reset()"
            plain
            round
            icon="el-icon-warning"
            :loading="loadingValue"
            size="mini"
          >重置</el-button>
        <el-button
            type="info"
            @click="buttonToggleSelect()"
            plain
            round
            icon="el-icon-check"
            :disabled="clickAble"
            :loading="loadingValue"
          >全部全选</el-button>
          <el-button
              type="info"
              @click="buttonToggleSelect(false)"
              plain
              round
              icon="el-icon-check"
              :disabled="clickAble"
              :loading="loadingValue"
          >全部反选</el-button>
            <el-button
              type="success"
              @click="showCase(reset=true)"
              plain
              round
              icon="el-icon-refresh"
              :disabled="clickAble"
              :loading="loadingValue"
          >刷新用例</el-button>
          </el-form-item>

      </el-form>
      <template>
        <div v-if="showProgressBar">
          <h
            style="font-size: 12px; font-color: #506266;"
          >成功: 【{{passed}}】 || 失败：【{{failed}}】 || 总计：【{{passed+failed}}】 || 成功率：【{{successRate}}】</h>
          <el-progress
            :text-inside="true"
            :stroke-width="12"
            :percentage="progressPercent"
            :color="colored"
            type="line"
            style="margin-right: 30px; margin-left: 0; font-size: 5px;"
          ></el-progress>
          <br />
        </div>
      </template>
      <template>
        <el-table
          ref="multipleCase"
          @select="handleSelected"
          @select-all="handleSelected"
          :data="tableData"
          class="case-table"
          height="368"
          :border="true"
          :stripe="true"
          size="mini"
          :highlight-current-row="true"
          style="font-size: 12px"
          :header-cell-style="{background:'#28ced1', color:'#506266'}"
        >
          <el-table-column type="selection" :selectable="isAble" disabled="true"></el-table-column>
          <el-table-column
            prop="number"
            label="序号"
            :sortable="true"
            align="center"
            class="col-case"
            :show-overflow-tooltip="true"
          ></el-table-column>
          <el-table-column
            prop="casename"
            label="用例名称"
            :sortable="true"
            align="center"
            class="col-case"
            :show-overflow-tooltip="true"
          ></el-table-column>
          <el-table-column
            prop="casefunc"
            label="用例方法"
            :sortable="true"
            align="center"
            class="col-case"
            :show-overflow-tooltip="true"
          ></el-table-column>
          <el-table-column
            prop="caseType"
            label="分组"
            :sortable="true"
            align="center"
            :show-overflow-tooltip="true"
            class="col-case"
          ></el-table-column>
          <!-- <el-table-column
            prop="remark"
            label="备注"
            :sortable="true"
            align="center"
            :show-overflow-tooltip="true"
            class="col-case"
          ></el-table-column> -->
          <el-table-column
            prop="operation"
            label="操作"
            :sortable="true"
            :show-overflow-tooltip="true"
            align="center"
            class="col-case"
          >

            <template slot-scope="scope">
              <el-tooltip
                class="item"
                effect="dark"
                content="点击后即可执行本条用例"
                placement="top"
                :hide-after="5000"
                :enterable="false"
              >
                <el-button
                  size="mini"
                  type="primary"
                  @click="onTest('caseForm', single=true, singleCase=scope.row.casefunc)"
                  style="font-size: 12px"
                  icon="el-icon-s-operation"
                  :disabled="clickAble"
                ></el-button>
              </el-tooltip>
            </template>
          </el-table-column>
          <el-table-column
            label="创建时间"
            prop="createTime"
            :sortable="true"
            align="center"
            :show-overflow-tooltip="true"
            class="col-case"
          ></el-table-column>
        </el-table>
      </template>
      <br />
      <template>
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :page-sizes="[8, 10, 25, 50, 100, 200]"
          :current-page="currentPage"
          :page-size="pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="caseTableData.length"
          :small="false"
          :background="true"
          :pager-count="5"
        ></el-pagination>
      </template>
      <br />
      <template>
        <el-form
          :inline="true"
          :model="searchCaseForm"
          ref="searchCaseForm"
          class="form-auto"
          size="mini"
        >
          <!-- <el-form-item>
            <el-tooltip class="item" effect="dark" placement="top">
              <div slot="content">
                搜索用例名后执行，
                <br />可以搜索多条用例同时执行
              </div>
              <el-button
                type="primary"
                @click="onSearchTest()"
                plain
                round
                icon="el-icon-video-camera"
                :loading="loadingValue"
                :disabled="clickAble"
              >执行搜索</el-button>
            </el-tooltip>
            <el-button
              @click="addNewcase"
              type="primary"
              plain
              round
              icon="el-icon-circle-plus-outline"
              :disabled="clickAble"
              :loading="loadingValue"
            >新增搜索</el-button>
          </el-form-item> -->
          <!-- <el-form-item style="margin-left: 0;">
            <el-button
              type="info"
              @click="buttonToggleSelect()"
              plain
              round
              icon="el-icon-check"
              :disabled="clickAble"
              :loading="loadingValue"
            >全部全选</el-button>
            <el-button
              type="info"
              @click="buttonToggleSelect(false)"
              plain
              round
              icon="el-icon-check"
              :disabled="clickAble"
              :loading="loadingValue"
            >全部反选</el-button>
            <el-button
              type="success"
              @click="showCase(reset=true)"
              plain
              round
              icon="el-icon-refresh"
              :disabled="clickAble"
              :loading="loadingValue"
            >刷新用例</el-button>
          </el-form-item> -->
          <br />
          <!-- <el-form-item
            v-for="(newcase, index) in searchCaseForm.newcases"
            :label="'用例: '"
            :key="newcase.key"
            :prop="'newcases.' + (index) + '.searchCasename'"
            :rules="{
      required: true, message: '不能为空', trigger: 'blur'
    }"
          >
            <el-select
              v-model="newcase.searchCasename"
              clearable
              filterable
              placeholder="下拉选择或直接搜索"
              no-data-text="请输入或选择用例名"
            >
              <el-option
                v-for="item in searchCaseForm.allCasename"
                :key="item.value"
                :label="item.name"
                :value="item.value"
              ></el-option>
            </el-select>
            <span v-if="index!==0">
              <el-tooltip class="item" effect="dark" content="移除当前新增项" placement="top">
                <el-button
                  @click.prevent="removeNewcase(newcase)"
                  type="danger"
                  plain
                  round
                  icon="el-icon-remove-outline"
                  :loading="loadingValue"
                  :disabled="clickAble"
                ></el-button>
              </el-tooltip>
            </span>
          </el-form-item> -->
        </el-form>
      </template>
      <br />
    </div>
  </div>
</template>

<script>
import headTop from '@/components/headTop'
import { baseUrl } from '@/config/env'
import { showLoading, hideLoading } from '@/config/common'
import {
  backendManageRunTest,
  backendManageQueryCaseTested,
  getLoginResult,
  initLoginResult,
  queryGroupCase,
  backendManageQueryCasename,
  backendManageQuerygroup,
  backendManageQueryenv
} from '@/api/getData'
export default {
  data () {
    return {
      caseRules: {
        env: [{ required: true, message: '请选择归属环境', trigger: 'blur' }]
      },
      return_list: [],
      return_env_list: [],
      passed: 0,
      failed: 0,
      rowSelected: [],
      loadingValue: false,
      multipleSelection: [],
      currentPage: 1,
      pageSize: 8,
      caseList: [],
      showProgressBar: false,
      colored: '',
      progressPercent: 0,
      setIntervalId: 0,
      searchCaseForm: {
        allCasename: [],
        newcases: [
          {
            searchCasename: ''
          }
        ]
      },
      caseForm: {
        env: '',
        // dataFrom: "database",
        group: ['全部'],
        openapi: '',
        description: ''
        // perform_num: 1
      },
      caseTableData: [],
      casename: [],
      casenameAfter: [],
      afterTrack: '',
      caseTotal: '',
      allSelect: false,
      singleAll: false,
      isSelectAll: false,
      loginIntervalId: 0,
      loginResult: '',
      successRate: 0,
      loginDesc: '',
      scanTimes: 0
    }
  },
  watch: {
    changeData: {
      handler (newName, oldName) {
        this.rowSelected.forEach(row => {
          this.toggleSelection([this.caseTableData[row]])
        })
      },
      deep: true,
      immediate: true
    }
  },
  computed: {
    changeData () {
      const { pageSize, currentPage } = this
      return {
        pageSize,
        currentPage
      }
    },
    tableData: function () {
      return this.caseTableData.slice(
        (this.currentPage - 1) * this.pageSize,
        this.currentPage * this.pageSize
      )
    },
    clickAble: function () {
      return this.setIntervalId !== 0
    },
    foolSelect: function () {
      return !!this.afterTrack
    }
  },
  components: {
    headTop
  },
  created: function () {
    this.showCase()
    this.getGroupName()
    this.getEnvName()
  },
  methods: {
    async getEnvName () {
      showLoading()
      try {
        const resp = await backendManageQueryenv()
        if (resp.code === 0) {
          this.return_env_list = resp.data
          // this.$message({
          //   type: 'success',
          //   showClose: true,
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
    async getGroupName () {
      showLoading()
      try {
        const resp = await backendManageQuerygroup()
        if (resp.code === 0) {
          this.return_list = resp.data
          // this.$message({
          //   type: 'success',
          //   showClose: true,
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
    async onQueryGroupCase () {
      showLoading()
      try {
        this.caseTableData.length = 0
        const resp = await queryGroupCase({
          callfunc: 'onQueryGroupCase',
          group: this.caseForm.group,
          env: this.caseForm.env || 'all'
        })
        if (resp.ResCode === 0) {
          resp.query_case_data.forEach((item, index) => {
            const data = {}
            const operation = {}
            let caseData = {}
            caseData.name = data.casename = item.fields.case_name
            caseData.value = data.casefunc = item.fields.case_func
            data.caseType = item.fields.case_type
            data.remark = item.fields.remark
            data.createTime = item.fields.create_time
            operation.key = ''
            data.operation = operation
            data.number = index + 1
            this.caseTableData.push(data)
            this.searchCaseForm.allCasename.push(caseData)
          })
          this.$message({
            type: 'success',
            showClose: true,
            message:
              '初始化用例列表成功, 共计 ' +
              this.caseTableData.length +
              ' 条用例'
          })
        } else {
          this.caseTableData.push()
          this.$notify.error({
            title: 'ERROR',
            message: resp.ErrMsg,
            offset: 288
          })
        }
      } catch (err) {
        this.$message.error(err.message)
      } finally {
        hideLoading()
      }
    },
    removeNewcase (item) {
      var index = this.searchCaseForm.newcases.indexOf(item)
      if (index !== -1) {
        this.searchCaseForm.newcases.splice(index, 1)
      }
    },
    addNewcase () {
      this.searchCaseForm.newcases.push({
        value: '',
        key: Date.now()
      })
    },
    showAllcase () {
      return this.searchCaseForm.allCasename
    },
    caseTotalFunc: function () {
      return this.casename.length === 0
        ? this.caseTableData.length
        : this.casename.length
    },
    isAble () {
      return this.setIntervalId === 0
    },
    buttonToggleSelect (selection = true) {
      this.afterTrack = false
      this.singleAll = true
      var allRow = []
      for (let i = 0; i < this.caseTableData.length; i++) {
        if (selection === true) {
          this.toggleSelection([this.caseTableData[i]], (selection = true))
          allRow.push(i)
        } else if (selection === false) {
          this.toggleSelection([this.caseTableData[i]], (selection = false))
        }
      }
      if (selection === true) {
        this.rowSelected = Array.from(new Set(allRow))
        this.allSelect = true
        this.isSelectAll = true
      } else {
        this.isSelectAll = false
        this.rowSelected.length = 0
        this.allSelect = false
      }
      this.casename.length = 0
    },
    toggleSelection (rows, selection = true) {
      this.$nextTick(function () {
        if (rows) {
          rows.forEach(row => {
            this.$refs.multipleCase.toggleRowSelection(row, selection)
          })
        } else {
          this.$refs.multipleCase.clearSelection()
        }
      })
    },
    handleSelected (selection) {
      this.multipleSelection = selection
      this.singleAll = false
      let rows = []
      let _casename = []
      this.multipleSelection.forEach(item => {
        rows.push(item.number - 1)
        _casename.push(item.casefunc)
      })
      this.rowSelected = Array.from(new Set(rows))
      this.casename = Array.from(new Set(_casename))
      this.casenameAfter = Array.from(new Set(_casename))
      if (this.casenameAfter.length === 0) {
        this.afterTrack = true
      } else {
        this.allSelect = true
        this.afterTrack = false
      }
    },
    async showCase (reset = false) {
      showLoading()
      if (reset === true) {
        this.$refs.caseForm.resetFields()
      }
      try {
        const params = { casefunc: 'showCase', page_type: 'caselist' }
        this.caseTableData.length = 0
        const resp = await backendManageQueryCasename(params)
        if (resp.ResCode === 0) {
          resp.query_case_data.forEach((item, index) => {
            const data = {}
            const operation = {}
            let caseData = {}
            caseData.name = data.casename = item.fields.case_name
            caseData.value = data.casefunc = item.fields.case_func
            data.caseType = item.fields.case_type
            data.caseEnv = item.fields.case_env
            data.remark = item.fields.remark
            data.createTime = item.fields.create_time
            operation.key = ''
            data.operation = operation
            data.number = index + 1
            this.caseTableData.push(data)
            this.searchCaseForm.allCasename.push(caseData)
          })
          this.$message({
            showClose: true,
            type: 'success',
            message:
              '初始化用例列表成功, 共计 ' +
              this.caseTableData.length +
              ' 条用例'
          })
        } else {
          this.$notify.error({
            title: 'ERROR',
            message: '载入用例列表失败',
            offset: 288
          })
        }
      } catch (err) {
        this.$message.error(err.message)
      } finally {
        hideLoading()
      }
    },
    caseMessageBox () {
      this.$confirm('您未选择用例, 默认将执行全部用例, 是否继续?', '提示', {
        confirmButtonText: '继续',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          this.caseRun()
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '已取消执行'
          })
        })
    },
    onSearchTest (
      caseForm = 'caseForm',
      searchCaseForm = 'searchCaseForm',
      single = true,
      search = true
    ) {
      var validPass = true
      this.$refs[caseForm].validate(async valid => {
        if (valid) {
        } else {
          validPass = false
          this.$notify.error({
            title: 'ERROR',
            message: '亲，必填项不能为空哟',
            offset: 288
          })
        }
      })
      this.$refs[searchCaseForm].validate(async valid => {
        if (valid) {
        } else {
          validPass = false
          this.$notify.error({
            title: 'ERROR',
            message: '亲，必填项不能为空哟',
            offset: 288,
            center: true
          })
          validPass = false
        }
      })
      if (validPass) {
        this.caseRun((single = true), (search = true))
      }
    },
    async caseRun (single = false, search = false) {
      this.showProgressBar = false
      try {
        this.scanTimes = 0
        if (!search) {
          this.caseTotal = this.caseTotalFunc()
          var theCasename = this.casename.length === 0 ? [] : this.casename
        } else {
          var _theCasename = []
          var theCasename = []
          this.searchCaseForm.newcases.forEach((item, index) => {
            _theCasename.push(item.searchCasename)
          })
          theCasename = Array.from(new Set(_theCasename))
          this.caseTotal = theCasename.length
          if (_theCasename.length !== theCasename.length) {
            this.$notify({
              title: '警告',
              message: '您搜索执行时，所选择的用例有重复！',
              position: 'bottom-left',
              type: 'warning',
              center: true
            })
            return
          }
        }
        // if (this.caseForm.perform_num === '') {
        //   this.caseForm.perform_num = 1
        // }
        const params = {
          group: this.caseForm.group,
          // corenum: this.caseForm.perform_num,
          env: this.caseForm.env,
          casename: theCasename,
          callfunc: 'onTest',
          desc: this.caseForm.description
        }
        initLoginResult()
        const result = await backendManageRunTest(params)
        if (result.ResCode === 0) {
          this.$message({
            type: 'success',
            message:
              '执行成功, 请等待测试完成, 报告编号(UUID): ' + result.report_id,
            duration: 0,
            showClose: true,
            center: true
          })
          this.loginIntervalId = setInterval(() => {
            this.freshLoginResult(single)
          }, 500)
          const data = {
            report_id: result.postData.report_id
          }
          this.setIntervalId = setInterval(() => {
            this._backendManageQueryCaseTested(data, single)
          }, 2000)
        } else {
          this.$message.error(result.ErrMsg)
        }
      } catch (err) {
        this.loadingValue = false
        this.$message.error(err.message)
      }
    },
    async freshLoginResult (single) {
      try {
        const resp = await getLoginResult({ 'js func': 'freshLoginResult' })
        if (resp.ResCode === 0) {
          const query_data = resp.query_data
          if (query_data.result !== 'init') {
            this.loginResult = query_data.result
            this.loginDesc = query_data.desc
            if (this.loginResult === 'failure') {
              this.$message({
                type: 'error',
                message: '登陆失败: ' + this.loginDesc,
                duration: 0,
                showClose: true,
                align: 'center'
              })
              window.clearInterval(this.setIntervalId)
              this.setIntervalId = 0
              this.loadingValue = false
              this.rememberCasename(single)
              window.open(`${baseUrl}/static/login.png`)
            } else {
              this.loadingValue = true
              this.progressPercent = 0
              this.showProgressBar = true
            }
            window.clearInterval(this.loginIntervalId)
          } else {
          }
        } else {
          this.$message.error(resp.ErrMsg || '获取登陆详情失败...')
        }
      } catch (err) {
        this.$message.error(err.message)
      }
    },
    async onTest (caseForm, single = false, singleCase = '') {
      this.$refs[caseForm].validate(async valid => {
        try {
          if (valid) {
            if (!single) {
              if (
                (this.casename.length === 0 && !this.allSelect) ||
                this.foolSelect
              ) {
                this.caseMessageBox()
              } else {
                this.caseRun()
              }
            } else {
              this.casename.length = 0
              this.casename.push(singleCase)
              this.caseRun((single = true))
            }
          } else {
            this.$notify.error({
              title: 'ERROR',
              message: '亲，必填项不能为空哟',
              offset: 288
            })
            return false
          }
        } catch (err) {
          this.$message.error(err.message)
        }
      })
    },
    reset () {
      this.showProgressBar = false
      this.buttonToggleSelect(false)
      this.$refs.caseForm.resetFields()
      this.$refs.searchCaseForm.resetFields()
      this.$message({
        showClose: true,
        type: 'success',
        message: '已清除'
      })
    },
    handleSizeChange (val) {
      showLoading()
      // console.log(`每页 ${val} 条`);
      this.pageSize = val
      hideLoading()
    },
    handleCurrentChange (val) {
      showLoading()
      this.currentPage = val
      hideLoading()
    },
    async _backendManageQueryCaseTested (data, single) {
      try {
        const resp = await backendManageQueryCaseTested(data)
        var count = resp.case_tested_count
        this.passed = resp.pass_count
        this.failed = resp.fail_count
        this.successRate = `${(
          (this.passed / (this.passed + this.failed)) *
          100
        ).toFixed(2)}%`
        this.scanTimes += 1
        if (this.scanTimes === 900) {
          window.clearInterval(this.setIntervalId)
          this.setIntervalId = 0
          this.$message({
            type: 'warning',
            message: '超时！系统遇到不可预估的异常, 进度计算未正常结束',
            duration: 0,
            showClose: true
          })
          this.loadingValue = false
          this.rememberCasename(single)
        }
        if (count === this.caseTotal) {
          this.progressPercent = 100
          this.colored = '#32CD32'
          this.$message({
            showClose: true,
            type: 'success',
            message: '测试完成, 共执行' + this.caseTotal + '条用例',
            duration: 5000
          })
          this.loadingValue = false
          this.rememberCasename(single)
          window.clearInterval(this.setIntervalId)
          this.setIntervalId = 0
        } else {
          this.progressPercent =
            Math.round((count / this.caseTotal) * 10000) / 100
          if (this.progressPercent < 50) {
            this.colored = '#C71585'
          } else if (this.progressPercent >= 50 < 100) {
            this.colored = '#8B008B'
          } else {
          }
        }
      } catch (err) {
        this.$message.error(err.message)
      }
    },
    rememberCasename (single) {
      if (single) {
        this.casename = []
        for (let i = 0; i < this.casenameAfter.length; i++) {
          this.casename.push(this.casenameAfter[i])
        }
        if (this.singleAll) {
          this.casename.length = 0
        }
      } else {
        if (!this.isSelectAll) {
          this.casename = []
          this.allSelect = false
          if (!this.singleAll) {
            this.casename = []
            for (let i = 0; i < this.casenameAfter.length; i++) {
              this.casename.push(this.casenameAfter[i])
            }
          }
        }
      }
    }
  }
}
</script>

<style lang="less" scoped>
@import "../style/mixin";
.case-table {
  max-height: 100%;
  width: 98%;
  min-width: 680px;
}
.col-report {
  background-color: rgba(2, 17, 3, 0.788);
}
.el-button--info.is-plain {
    color: #67C23A;
    background: #f0f9eb;
    border-color: #d3d4d6;
}

</style>
