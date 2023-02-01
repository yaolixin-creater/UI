<template>
  <div>
    <head-top></head-top>
    <div style="margin-left: 20px; margin-top: 20px; font-size: 14px">
      <el-form
        :inline="true"
        :model="reportForm"
        ref="reportForm"
        class="form-report"
        label-width="80px"
        size="mini"
      >
        <el-form-item label="报告编号" :required="false" prop="reportId">
          <el-input v-model="reportForm.reportId" placeholder="请输入" clearable size="mini">
            <i slot="suffix" class="el-input__icon el-icon-search"></i>
          </el-input>
        </el-form-item>
        <el-form-item label="归属环境" :required="false" prop="env">
          <el-select v-model="reportForm.env" clearable filterable size="mini">
            <el-option
              v-for="item in return_env_list"
              :key="item.Env_name"
              :label="item.desc"
              :value="item.Env_name"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="报告描述" :required="false" prop="desc">
          <el-input v-model="reportForm.desc" placeholder="请输入" clearable size="mini">
            <i slot="suffix" class="el-input__icon el-icon-search"></i>
          </el-input>
        </el-form-item>
        <el-form-item label="时间范围" prop="timeRange" :required="false">
          <el-date-picker
            v-model="reportForm.timeRange"
            type="datetimerange"
            align="center"
            :unlink-panels="true"
            range-separator="至"
            start-placeholder="开始时间"
            end-placeholder="结束时间"
            format="yyyy-MM-dd HH:mm:ss"
            value-format="yyyy-MM-dd HH:mm:ss"
            :default-time="['00:00:00','23:59:59']"
            :picker-options="pickerOptions"
            size="mini"
            :time-arrow-control="false"
            :clearable="true"
          ></el-date-picker>
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            @click="onQueryReport('reportForm')"
            plain
            round
            icon="el-icon-search"
            :loading="queryLoading"
            size="mini"
          >查询</el-button>
        </el-form-item>
        <el-form-item>
          <el-button
            type="danger"
            @click="reset()"
            plain
            round
            icon="el-icon-warning"
            size="mini"
          >重置</el-button>
        </el-form-item>
      </el-form>
      <el-table
        :data="tableData"
        class="report-table"
        height="432"
        :border="true"
        :stripe="true"
        size="mini"
        :highlight-current-row="true"
        style="font-size: 12px"
        :header-cell-style="{background:'#00ced1', color:'#506266'}"
      >
        <el-table-column type="index" align="center"></el-table-column>
        <el-table-column
          prop="reportId"
          label="报告编号"
          :sortable="true"
          align="center"
          :show-overflow-tooltip="true"
        ></el-table-column>
        <el-table-column
          prop="env_desc"
          label="HOST"
          :sortable="true"
          align="center"
          :show-overflow-tooltip="true"
        ></el-table-column>
        <el-table-column
          prop="desc"
          label="用例执行"
          :sortable="true"
          align="center"
          :show-overflow-tooltip="true"
        ></el-table-column>
        <el-table-column
          prop="remark"
          label="测试描述"
          :sortable="true"
          align="center"
          :show-overflow-tooltip="true"
        ></el-table-column>
        <el-table-column
          prop="operation"
          label="操作"
          :sortable="true"
          :show-overflow-tooltip="true"
          align="center"
          width="358px"
        >
          <template slot-scope="scope">
            <el-tooltip
              class="item"
              effect="light"
              content="测试概要"
              placement="top"
              :hide-after="5000"
              :enterable="false"
            >
              <el-button
                size="mini"
                type="success"
                @click="onQuerySummary(scope.row)"
                style="font-size: 10px"
                icon="el-icon-view"
              ></el-button>
            </el-tooltip>
            <el-tooltip
              class="item"
              effect="light"
              content="复制测试概要至剪贴板"
              placement="top"
              :hide-after="5000"
              :enterable="false"
            >
              <el-button
                size="mini"
                type="info"
                style="font-size: 10px"
                icon="el-icon-edit"
                @mouseover.native="copyMessage(scope.row)"
                v-clipboard:copy="summaryMessage"
                v-clipboard:success="successCopy"
                v-clipboard:error="errorCopy"
              ></el-button>
            </el-tooltip>
            <el-tooltip
              class="item"
              effect="light"
              content="测试报告"
              placement="top"
              :hide-after="5000"
              :enterable="false"
            >
              <a :href="scope.row.operation.url" target="_blank" class="buttonText">
                <el-button
                  size="mini"
                  type="primary"
                  style="font-size: 10px"
                  icon="el-icon-monitor"
                ></el-button>
              </a>
            </el-tooltip>
            <el-tooltip
              class="item"
              effect="light"
              content="删除此条报告"
              placement="top"
              :hide-after="5000"
              :enterable="false"
            >
              <el-button
                size="mini"
                type="danger"
                @click="reportMessageBox(scope.$index, scope.row)"
                style="font-size: 10px"
                icon="el-icon-delete"
              ></el-button>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column
          prop="createTime"
          label="创建时间"
          :sortable="true"
          align="center"
          :show-overflow-tooltip="true"
        >
          <template slot-scope="scope">
            <i class="el-icon-time"></i>
            <span style="margin-left: 5px">{{ scope.row.createTime }}</span>
          </template>
        </el-table-column>
      </el-table>
      <br />
      <template>
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :page-sizes="[10, 50, 100, 200, 400, 600, 1000, 10000]"
          :current-page="currentPage"
          :page-size="pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="reportTableData.length"
          :small="false"
          :background="true"
          :pager-count="6"
        ></el-pagination>
      </template>
      <br />
      <template>
        <el-dialog
          title="测试结果概要信息"
          :visible.sync="dialogTableVisible"
          :fullscreen="false"
          width="65%"
          style="padding: 0px 0px 0; text-align: center;"
        >
          <el-table
            :data="summaryTableData"
            height="468"
            :border="true"
            :stripe="true"
            size="mini"
            :highlight-current-row="true"
            style="font-size: 10px"
            :header-cell-style="{background:'#00cff1', color:'#506266'}"
          >
            <el-table-column
              prop="number"
              label="序号"
              :sortable="true"
              align="center"
              :show-overflow-tooltip="true"
            ></el-table-column>
            <el-table-column
              prop="casename"
              label="用例名称"
              :sortable="true"
              align="center"
              :show-overflow-tooltip="true"
            ></el-table-column>
            <el-table-column
              prop="TransactionID"
              label="响应码"
              :sortable="true"
              align="center"
              :show-overflow-tooltip="true"
            ></el-table-column>
            <el-table-column
              prop="desc"
              label="描述"
              :sortable="true"
              align="center"
              :show-overflow-tooltip="true"
            ></el-table-column>
            <el-table-column
              prop="err_msg"
              label="异常信息"
              :sortable="true"
              align="center"
              :show-overflow-tooltip="true"
            ></el-table-column>
            <el-table-column
              prop="createTime"
              label="创建时间"
              :sortable="true"
              align="center"
              :show-overflow-tooltip="true"
            >
              <template slot-scope="scope">
                <i class="el-icon-time"></i>
                <span style="margin-left: 5px">{{ scope.row.createTime }}</span>
              </template>
            </el-table-column>
          </el-table>
        </el-dialog>
      </template>
    </div>
  </div>
</template>

<script>
import headTop from '@/components/headTop'
import Vue from 'vue'
import { showLoading, hideLoading, pickerOptions } from '@/config/common'
import {
  backendManageQueryReport,
  backendManageDelReport,
  backendManageQuerySummary,
  backendManageQueryenv
} from '@/api/getData'
import { baseUrl } from '@/config/env'
export default {
  data () {
    return {
      return_env_list: [],
      pickerOptions,
      reportForm: {
        paramFiles: [],
        defaultEnv: 'test',
        timeRange: []
      },
      reportTableData: [],
      summaryItems: [],
      summaryTableData: [],
      summaryMessage: '',
      messages: '',
      summaryPassed: 0,
      summaryFailed: 0,
      dialogTableVisible: false,
      currentPage: 1,
      pageSize: 10,
      queryLoading: false
    }
  },
  computed: {
    tableData: function () {
      return this.reportTableData.slice(
        (this.currentPage - 1) * this.pageSize,
        this.currentPage * this.pageSize
      )
    }
  },
  components: {
    headTop
  },
  created: function () {
    this.getEnvName()
  },
  mounted: function () {
    this.onQueryReport('reportForm')
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
    successCopy (row) {
      this.$message.success({
        showClose: true,
        message: `复制内容至剪贴板成功！共${this.summaryItems.length}项概要信息...`,
        center: true
      })
      // this.summaryItems = [];
    },
    errorCopy () {
      this.$message.error({ message: '复制未成功...', center: true })
    },
    init () {
      this.reportTableData.length = 0
    },
    reportMessageBox (index, row) {
      this.$confirm('此操作将永久删除该报告, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          this.handleDelete(index, row)
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '已取消'
          })
        })
    },
    async handleDelete (index, row) {
      try {
        const resp = await backendManageDelReport({
          report_id: row.operation.report_id
        })
        if (resp.ResCode === 0) {
          this.$message({
            showClose: true,
            type: 'success',
            message: '删除成功'
          })
        } else {
          this.$message.error(resp.ErrMsg)
        }
      } catch (err) {
        this.$message({
          type: 'error',
          message: err.message
        })
      } finally {
        this.reportTableData.splice(index, 1)
      }
    },
    reset () {
      this.$refs.reportForm.resetFields()
      this.$message({
        showClose: true,
        type: 'success',
        message: '已清除'
      })
    },
    handleSizeChange (val) {
      // console.log(`每页 ${val} 条`);
      showLoading()
      this.pageSize = val
      hideLoading()
    },
    handleCurrentChange (val) {
      showLoading()
      this.currentPage = val
      // console.log(`当前页: ${val}`);
      hideLoading()
    },
    async copyMessage (row) {
      try {
        this.summaryMessage = ''
        this.summaryPassed = 0
        this.summaryFailed = 0
        this.summaryItems = []
        const resp = await backendManageQuerySummary({
          reportId: row.operation.report_id
        })
        if (resp.ResCode === 0) {
          resp.query_data.forEach((item, index) => {
            const data = {}
            data.number = index + 1 + ')'
            data.casename = item.fields.casename
            data.TransactionID = item.fields.TransactionID
            data.desc = item.fields.desc || '成功'
            data.err_msg = item.fields.err_msg
            data.filename = item.fields.filename
            data.env = item.fields.env
            data.result = item.fields.result
            // data.remark = item.fields.remark;
            if (data.result) {
              this.summaryPassed += 1
            } else {
              this.summaryFailed += 1
            }
            this.summaryItems.push(data)
            this.summaryMessage +=
              data.number +
              '  ' +
              // data.filename.split("/").pop() +
              // " " +
              data.casename +
              '  ' +
              data.desc +
              '  ' +
              data.TransactionID +
              // "  " +
              // data.err_msg +
              '  ' +
              '\r\n'
          })
        } else {
          this.$message.error(resp.ErrMsg)
          return
        }
        this.summaryMessage = `HOST：${row.operation.env_desc}; \r\n报告编号: ${
          row.operation.report_id
        }; \r\n后端管理测试报告链接: \r\n${baseUrl}/backendManage/getReport/test_report_${
          row.operation.report_id
        }.html\r\nTest result details: Passed: 【${
          this.summaryPassed
        }】; Failed: 【${this.summaryFailed}】; Total: 【${this.summaryFailed +
          this.summaryPassed}】
        \r\n\r\n${this.summaryMessage}`
        this.summaryPassed = 0
        this.summaryFailed = 0
        return this.summaryMessage
      } catch (err) {
        this.$message.error(err.messages)
      }
    },
    copyer () {
      const self = new Vue()
      this.$copyText(this.summaryMessage).then(
        function (action) {
          self.$message.success(
            `复制内容至剪贴板成功！共${self.summaryItems.length}项概要信息...`
          )
        },
        function (action) {
          self.$message.error('复制内容至剪贴板失败！可能不兼容该浏览器！')
        }
      )
    },
    async onQuerySummary (row) {
      showLoading()
      this.dialogTableVisible = true
      this.summaryTableData.length = 0
      try {
        const resp = await backendManageQuerySummary({
          reportId: row.operation.report_id
        })
        if (resp.ResCode === 0) {
          resp.query_data.forEach((item, index) => {
            const data = {}
            data.report_id = item.fields.report_id
            data.casename = item.fields.casename
            data.TransactionID = item.fields.TransactionID
            data.result = item.fields.result
            data.remark = item.fields.remark
            data.desc = item.fields.desc || '成功'
            data.createTime = item.fields.create_time
            // data.env = item.fields.env;
            data.err_msg = item.fields.err_msg
            data.number = index + 1
            this.summaryTableData.push(data)
          })
          this.$message({
            type: 'success',
            showClose: true,
            message:
              '查询成功, 共计 ' + this.summaryTableData.length + ' 条结果...'
          })
        } else {
          this.$message.error(resp.ErrMsg)
        }
      } catch (err) {
        this.$message({
          type: 'error',
          message: err.messages
        })
      } finally {
        hideLoading()
      }
    },
    async onQueryReport (reportForm) {
      this.queryLoading = true
      showLoading()
      try {
        this.init()
        var timeRange = this.reportForm.timeRange
        let timeInstance = ['2000-01-01 00:00:00', '3000-01-01 00:00:00']
        timeRange = timeRange != null ? timeRange : timeInstance
        timeRange = timeRange.length > 0 ? timeRange : timeInstance
        const params = {
          report_id: this.reportForm.reportId,
          env: this.reportForm.env,
          desc: this.reportForm.desc,
          start_time: timeRange[0],
          end_time: timeRange[1],
          funcname: 'onQueryReport'
        }
        const resp = await backendManageQueryReport(params)
        if (resp.ResCode === 0) {
          resp.data.forEach((item, index) => {
            const data = {}
            const operation = {}
            data.processBar = '已完成'
            operation.report_id = data.reportId = item.pk
            operation.env_desc = data.env_desc = item.fields.host
            data.desc = item.fields.desc
            data.remark = item.fields.remark
            data.createTime = item.fields.create_time
            operation.name = item.fields.name
            operation.url = baseUrl + item.fields.url
            data.operation = operation
            data.index = index
            this.reportTableData.push(data)
          })
          if (this.reportTableData.length === 0) {
            this.reportTableData = []
          }
          this.$message({
            type: 'success',
            showClose: true,
            message:
              '查询成功, 共计 ' + this.reportTableData.length + ' 条测试结果...'
          })
        } else {
          this.$message.error(resp.ErrMsg)
        }
      } catch (err) {
        this.$message({
          type: 'error',
          message: err.message
        })
      } finally {
        hideLoading()
        this.queryLoading = false
      }
    }
  }
}
</script>

<style lang="less" scoped>
@import "../style/mixin";
.report-table {
  max-height: 100%;
  width: 98%;
}
.col-report {
  background-color: rgba(2, 17, 3, 0.788);
}
</style>
