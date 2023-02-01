<template>
  <div>
    <head-top></head-top>
    <div style="margin-left: 20px; margin-top: 20px; font-size: 14px">
      <el-form
        :inline="true"
        :model="groupTableData"
        ref="groupTableData"
        class="form-group"
        label-width="80px"
        size="mini"
      >
        <el-form-item label="环境标识" :required="false" prop="groupId">
          <el-input v-model="searchGroupName" placeholder="请输入" clearable size="mini">
            <i slot="suffix" class="el-input__icon el-icon-search"></i>
          </el-input>
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            @click="onQuerygroup('groupTableData')"
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
            @click="centerDialogVisible = true"
            plain
            round
            icon="el-icon-plus"
            size="mini"
          >新增
          </el-button>
        </el-form-item>
      </el-form>
      <el-table
        :data="tableData"
        class="group-table"
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
          prop="groupId"
          label="环境编号"
          :sortable="true"
          align="center"
          :show-overflow-tooltip="true"
        ></el-table-column>
        <el-table-column
          prop="groupName"
          label="环境标识"
          :sortable="true"
          align="center"
          :show-overflow-tooltip="true"
        ></el-table-column>
        <el-table-column
          prop="owner"
          label="最后修改人"
          :sortable="true"
          align="center"
          :show-overflow-tooltip="true"
        ></el-table-column>
        <el-table-column
          prop="host"
          label="域名"
          :sortable="true"
          align="center"
          :show-overflow-tooltip="true"
        ></el-table-column>
        <el-table-column
          prop="desc"
          label="环境描述"
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
        >
          <template slot-scope="scope">
            <el-tooltip
              class="item"
              effect="light"
              content="修改"
              placement="top"
              :hide-after="5000"
              :enterable="false"
            >
              <el-button
                size="mini"
                type="success"
                @click="onShowStepArgvs(scope.row)"
                style="font-size: 10px"
                icon="el-icon-edit"
              ></el-button>
            </el-tooltip>
            <el-tooltip
              class="item"
              effect="light"
              content="删除"
              placement="top"
              :hide-after="5000"
              :enterable="false"
            >
            </el-tooltip>
            <el-tooltip
              class="item"
              effect="light"
              content="删除此环境"
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
      <template>
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :page-sizes="[10, 50, 100, 200, 400, 600, 1000, 10000]"
          :current-page="currentPage"
          :page-size="pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="groupTableData.length"
          :small="false"
          :background="true"
          :pager-count="6"
        ></el-pagination>
      </template>
      <br />
      <template>
        <el-dialog
              title="新增环境"
              :visible.sync="centerDialogVisible"
              width="30%"
              center>
              <el-input v-model="addGroupFrom.addGroupName" placeholder="请输入环境标识"></el-input>
              <el-input v-model="addGroupFrom.addGroupDesc" placeholder="请输入环境描述"></el-input>
              <el-input v-model="addGroupFrom.addGroupHost" placeholder="请输入环境对应的域名"></el-input>
              <span slot="footer" class="dialog-footer">
                <el-button @click="centerDialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="addgroup()">确 定</el-button>
              </span>
            </el-dialog>
      </template>
      <br />
      <template>
        <el-dialog
              :title="'【'+groupConfig+'】' + '的环境信息修改'"
              :visible.sync="centerDialogVisible2"
              width="30%"
              center>
              <el-input v-model="modGroupFrom.modGroupName" placeholder="请输入环境标识"></el-input>
              <el-input v-model="modGroupFrom.modGroupDesc" placeholder="请输入环境描述"></el-input>
              <el-input v-model="modGroupFrom.modGroupHost" placeholder="请输入环境对应的域名"></el-input>
              <span slot="footer" class="dialog-footer">
                <el-button @click="centerDialogVisible2 = false">取 消</el-button>
                <el-button type="primary" @click="modgroup()">确 定</el-button>
              </span>
            </el-dialog>
      </template>
    </div>
  </div>
</template>

<script>
import headTop from '@/components/headTop'
import { showLoading, hideLoading } from '@/config/common'
import {
  backendManageDelenv,
  backendManageQueryenvs,
  backendManagecreateenv,
  backendManagemodenv
} from '@/api/getData'
export default {
  data () {
    return {
      centerDialogVisible: false,
      centerDialogVisible2: false,
      groupConfig: '',
      addGroupFrom: {
        addGroupName: '',
        addGroupDesc: '',
        addGroupHost: ''
      },
      modGroupFrom: {
        modGroupName: '',
        modGroupDesc: '',
        modGroupHost: ''
      },
      searchGroupName: '',
      groupTableData: [],
      messages: '',
      currentPage: 1,
      pageSize: 10,
      queryLoading: false
    }
  },
  computed: {
    tableData: function () {
      return this.groupTableData.slice(
        (this.currentPage - 1) * this.pageSize,
        this.currentPage * this.pageSize
      )
    }
  },
  components: {
    headTop
  },
  mounted: function () {
    this.onQuerygroup()
  },
  methods: {
    init () {
      this.groupTableData.length = 0
    },
    handleSizeChange (val) {
      showLoading()
      this.pageSize = val
      hideLoading()
    },
    handleCurrentChange (val) {
      showLoading()
      this.currentPage = val
      hideLoading()
    },
    async handleDelete (index, row) {
      try {
        const resp = await backendManageDelenv({
          group_name: row.groupName
        })
        if (resp.code === 0) {
          this.$message({
            showClose: true,
            type: 'success',
            message: '删除成功'
          })
          this.groupTableData.splice(index, 1)
        } else {
          this.$message.error(resp.ErrMsg)
        }
      } catch (err) {
        this.$message({
          type: 'error',
          message: err.message
        })
      }
    },
    reportMessageBox (index, row) {
      this.$confirm('此操作将永久删除该环境, 是否继续?', '提示', {
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
    onShowStepArgvs (row) {
      try {
        this.groupConfig = row.groupName
        this.centerDialogVisible2 = true
      } catch (err) {
        this.$message({
          type: 'error',
          message: err.message
        })
      }
    },
    async modgroup () {
      showLoading()
      this.centerDialogVisible2 = false
      try {
        const data = {}
        data.group_name = this.groupConfig
        data.m_group_name = this.modGroupFrom.modGroupName
        data.m_group_desc = this.modGroupFrom.modGroupDesc
        data.m_group_host = this.modGroupFrom.modGroupHost
        const resp = await backendManagemodenv(data)
        if (resp.code === 0) {
          this.$message({
            showClose: true,
            type: 'success',
            message: '修改成功'
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
        this.onQuerygroup()
      }
    },
    async addgroup () {
      showLoading()
      this.centerDialogVisible = false
      try {
        const data = {}
        data.addGroupName = this.addGroupFrom.addGroupName
        data.addGroupDesc = this.addGroupFrom.addGroupDesc
        data.addGroupHost = this.addGroupFrom.addGroupHost
        data.addOwner = localStorage.getItem('autoUsernameForRemember')
        const resp = await backendManagecreateenv(data)
        if (resp.code === 0) {
          this.$message({
            showClose: true,
            type: 'success',
            message: '添加成功'
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
        this.onQuerygroup()
      }
    },
    async onQuerygroup () {
      this.queryLoading = true
      showLoading()
      try {
        this.init()
        const data2 = {}
        data2.search_group_name = this.searchGroupName
        const resp = await backendManageQueryenvs(data2)
        if (resp.code === 0) {
          resp.data.forEach((item, index) => {
            const data = {}
            const operation = {}
            data.processBar = '已完成'
            operation.groupId = data.groupId = item.Env_id
            operation.groupName = data.groupName = item.Env_name
            data.owner = item.owner
            data.desc = item.desc
            data.host = item.host
            data.createTime = item.create_time
            data.operation = operation
            data.index = index
            this.groupTableData.push(data)
          })
          if (this.groupTableData.length === 0) {
            this.groupTableData = []
          }
          this.$message({
            showClose: true,
            type: 'success',
            message:
              '查询成功, 共计 ' + this.groupTableData.length + ' 条环境...'
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
.group-table {
  max-height: 100%;
  width: 98%;
}
.col-group {
  background-color: rgba(2, 17, 3, 0.788);
}
</style>
