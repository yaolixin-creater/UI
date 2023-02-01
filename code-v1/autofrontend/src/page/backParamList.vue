<template>
  <div>
    <head-top></head-top>
    <div style="margin-left: 20px; margin-top: 20px; font-size: 14px">
      <el-form
        :inline="true"
        :model="resourceForm"
        ref="resourceForm"
        style="margin-left: 0px;"
        size="mini"
        label-position="right"
        label-width="86px"
      >
        <el-form-item label="用例名称" prop="casename" :required="false">
          <el-select
            v-model="resourceForm.casename"
            clearable
            filterable
            size="mini"
            no-data-text
            @visible-change="onQuerySingleCaselist()"
            style="width: 258px;"
          >
            <el-option
              v-for="item in resourceForm.searchCaseList"
              :key="item.casename"
              :label="item.casename"
              :value="item.casefunc"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="用例类型" :required="false" prop="caseType">
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
        <el-form-item label="时间范围" prop="timeRange" :required="false">
          <el-date-picker
            v-model="resourceForm.timeRange"
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
        <el-form-item label="备注" :required="false" prop="caseRemark">
          <el-input
            v-model="resourceForm.caseRemark"
            placeholder="请输入"
            clearable
            style="width: 258px;"
            size="mini"
          ></el-input>
        </el-form-item>
        <el-form-item>
          <el-button
            type="success"
            @click="onQueryCasename()"
            round
            plain
            icon="el-icon-refresh"
            :loading="queryLoading"
            size="mini"
          >查询</el-button>
        </el-form-item>
        <el-form-item>
          <el-button
            type="danger"
            @click="resetForm()"
            plain
            round
            icon="el-icon-edit"
            size="mini"
          >重置</el-button>
        </el-form-item>
      </el-form>
      <div class="param_table">
        <el-table
          class="resource_table"
          :data="tableData"
          height="433"
          :border="true"
          :stripe="true"
          size="mini"
          :highlight-current-row="true"
          style="font-size: 12px"
          :header-cell-style="{background:'#00ced1', color:'#506266'}"
          :default-expand-all="false"
        >
          <el-table-column
            label="序号"
            :sortable="true"
            align="center"
            class="col-case"
            :show-overflow-tooltip="true"
            type="index"
          ></el-table-column>
          <el-table-column
            prop="casename"
            label="用例名称"
            align="center"
            class="col-report"
            :show-overflow-tooltip="true"
          ></el-table-column>
          <el-table-column
            prop="casefunc"
            label="用例方法"
            align="center"
            class="col-report"
            :show-overflow-tooltip="true"
          ></el-table-column>
          <el-table-column
            prop="caseType"
            label="用例类型"
            align="center"
            :show-overflow-tooltip="true"
            class="col-report"
          ></el-table-column>
          <el-table-column
            prop="remark"
            label="备注"
            align="center"
            class="col-report"
            :show-overflow-tooltip="true"
          ></el-table-column>
          <el-table-column
            prop="operation"
            label="操作"
            :show-overflow-tooltip="true"
            align="center"
            class="col-report"
            width="358px"
          >
            <template slot-scope="scope">
              <el-tooltip
                class="item"
                effect="light"
                content="用例参数编辑"
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
                content="新增用例"
                placement="top"
                :hide-after="5000"
                :enterable="false"
              >
                <el-button
                  size="mini"
                  type="info"
                  style="font-size: 10px"
                  icon="el-icon-plus"
                  @click="paramAddFunc()"
                ></el-button>
              </el-tooltip>
              <el-tooltip
                class="item"
                effect="light"
                content="删除用例和用例下的所有步骤"
                placement="top"
                :hide-after="5000"
                :enterable="false"
              >
                <el-button
                  size="mini"
                  type="danger"
                  style="font-size: 10px"
                  icon="el-icon-delete"
                  @click="resourceMessageBox(scope.$index, scope.row, delCase=true)"
                ></el-button>
              </el-tooltip>
            </template>
          </el-table-column>
          <el-table-column
            prop="createTime"
            label="创建时间"
            :sortable="true"
            align="center"
            class="col-report"
            :show-overflow-tooltip="true"
          >
            <template slot-scope="scope">
              <i class="el-icon-time"></i>
              <span style="margin-left: 5px">{{ scope.row.createTime }}</span>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <br />
      <template>
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :page-sizes="[10, 20, 50, 100, 200, 400, 600, 1000, 10000]"
          :current-page="currentPage"
          :page-size="pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="caseTableData.length"
          :small="false"
          :background="true"
          :pager-count="6"
        ></el-pagination>
      </template>
      <template>
        <el-dialog
          :title="'【'+caseConfig+'】' + '**步骤参数修改'"
          :visible.sync="dialogStepTableVisible"
          class="table-dialog"
          :fullscreen="false"
          width="90%"
          style="text-align: center;"
        >
          <el-table
            class="step_resource_table"
            :data="stepTableData"
            ref="stepTableData"
            height="438"
            :border="true"
            :stripe="true"
            size="mini"
            :highlight-current-row="true"
            style="font-size: 10px"
            :header-cell-style="{background:'#cacfdb', color:'#506266'}"
          >
            <el-table-column type="index" align="center"></el-table-column>
            <el-table-column
              label="动作方法"
              prop="eleAction"
              align="center"
              :show-overflow-tooltip="true"
            ></el-table-column>
            <el-table-column
              label="动作描述"
              prop="actionDesc"
              align="center"
              :show-overflow-tooltip="true"
            ></el-table-column>
            <el-table-column
              label="用例步骤"
              prop="stepSequence"
              :sortable="false"
              align="center"
              :show-overflow-tooltip="true"
            ></el-table-column>
            <el-table-column
              label="定位方式"
              prop="locateType"
              align="center"
              :show-overflow-tooltip="true"
            ></el-table-column>
            <el-table-column
              label="定位元素值"
              prop="locateValue"
              align="center"
              :show-overflow-tooltip="true"
            ></el-table-column>
            <el-table-column
              label="动作参数"
              prop="actionValue"
              align="center"
              :show-overflow-tooltip="true"
            ></el-table-column>
            <el-table-column
              label="动作断言值"
              prop="assertValue"
              align="center"
              :show-overflow-tooltip="true"
            ></el-table-column>
            <el-table-column
              label="扩展参数"
              prop="extendArgvs"
              align="center"
              :show-overflow-tooltip="true"
            ></el-table-column>
            <el-table-column
              label="步骤操作"
              width="436"
              prop="operation"
              align="center"
              class="col-report"
              :show-overflow-tooltip="true"
            >
              <template slot-scope="scope">
                <el-tooltip
                  class="item"
                  effect="light"
                  content="上移"
                  placement="top"
                  :hide-after="5000"
                  :enterable="false"
                >
                  <el-button
                    size="mini"
                    type="danger"
                    style="font-size: 10px"
                    round
                    icon="el-icon-top"
                    :disabled="scope.$index === 0"
                    @click="onStepMove(scope.$index, scope.row)"
                  ></el-button>
                </el-tooltip>
                <el-tooltip
                  class="item"
                  effect="light"
                  content="下移"
                  round
                  :hide-after="5000"
                  :enterable="false"
                >
                  <el-button
                    size="mini"
                    type="danger"
                    :disabled="scope.$index === (stepTableData.length-1)"
                    style="font-size: 10px"
                    round
                    icon="el-icon-bottom"
                    @click="onStepMove(scope.$index, scope.row, up=false)"
                  ></el-button>
                </el-tooltip>
                <el-tooltip
                  class="item"
                  effect="light"
                  content="修改当前项参数"
                  placement="top"
                  :hide-after="5000"
                  :enterable="false"
                >
                  <el-button
                    size="mini"
                    type="info"
                    @click="onEditStepArgvs(scope.row)"
                    style="font-size: 10px"
                    icon="el-icon-edit"
                    round
                  ></el-button>
                </el-tooltip>
                <el-tooltip
                  class="item"
                  effect="light"
                  :hide-after="5000"
                  :enterable="false"
                  :content="'插入步骤，默认为第【' + (scope.$index + 1) + '】步'"
                >
                  <el-button
                    size="mini"
                    type="primary"
                    style="font-size: 10px"
                    icon="el-icon-plus"
                    round
                    @click="onNewStepArgvs(scope.$index, scope.row)"
                  ></el-button>
                </el-tooltip>
                <el-tooltip
                  class="item"
                  effect="light"
                  :content="'删除第【' + (scope.$index + 1) + '】个步骤'"
                  placement="top"
                  :hide-after="5000"
                  :enterable="false"
                >
                  <el-button
                    size="mini"
                    type="danger"
                    @click="resourceMessageBox(scope.$index, scope.row)"
                    style="font-size: 10px"
                    round
                    icon="el-icon-minus"
                  ></el-button>
                </el-tooltip>
                <el-tooltip
                  class="item"
                  effect="light"
                  :content="'导入数据表中步骤作为第【' + (scope.$index + 1) + '】个步骤'"
                  placement="top"
                  :hide-after="5000"
                  :enterable="false"
                >
                  <el-button
                    size="mini"
                    type="success"
                    style="font-size: 10px"
                    round
                    icon="el-icon-circle-plus"
                    @click="onQueryForImport(scope.row)"
                  ></el-button>
                </el-tooltip>
              </template>
            </el-table-column>
          </el-table>
        </el-dialog>
      </template>
      <template>
        <el-dialog
          :title="importStepTitle"
          :visible.sync="dialogAllStepTableVisible"
          class="table-dialog"
          :fullscreen="false"
          width="65%"
          style="text-align: center;"
        >
          <el-form
            :inline="true"
            :model="importSearchForm"
            ref="importSearchForm"
            label-width="88px"
            size="mini"
            label-position="right"
          >
            <el-form-item label="动作描述" :required="false" prop="actionDesc">
              <el-select
                v-model="importSearchForm.actionDesc"
                clearable
                filterable
                size="mini"
                no-data-text
                @visible-change="generatorDescList()"
                @change="queryStepAccordDesc()"
                class="argvForm"
              >
                <el-option
                  v-for="item in importSearchForm.descList"
                  :key="item.key"
                  :label="item.value"
                  :value="item.value"
                ></el-option>
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button
                size="mini"
                type="success"
                style="font-size: 10px"
                round
                icon="el-icon-refresh"
                @click="queryStepAccordDesc()"
              >刷新</el-button>
            </el-form-item>
          </el-form>
          <el-table
            class="step_resource_table"
            :data="importStepTableData"
            ref="importStepTableData"
            height="438"
            :border="true"
            :stripe="true"
            size="mini"
            :highlight-current-row="true"
            style="font-size: 10px"
            :header-cell-style="{background:'#cacfdb', color:'#506266'}"
          >
            <el-table-column type="index" align="center"></el-table-column>
            <el-table-column
              label="动作方法"
              prop="eleAction"
              align="center"
              :show-overflow-tooltip="true"
              :sortable="true"
            ></el-table-column>
            <el-table-column
              label="动作描述"
              prop="actionDesc"
              align="center"
              :show-overflow-tooltip="true"
              :sortable="true"
            ></el-table-column>
            <el-table-column
              label="用例步骤"
              prop="stepSequence"
              align="center"
              :show-overflow-tooltip="true"
              :sortable="true"
            ></el-table-column>
            <el-table-column
              label="定位方式"
              prop="locateType"
              align="center"
              :show-overflow-tooltip="true"
              :sortable="true"
            ></el-table-column>
            <el-table-column
              label="定位元素值"
              prop="locateValue"
              align="center"
              :show-overflow-tooltip="true"
              :sortable="true"
            ></el-table-column>
            <el-table-column
              label="动作参数"
              prop="actionValue"
              align="center"
              :show-overflow-tooltip="true"
              :sortable="true"
            ></el-table-column>
            <el-table-column
              label="动作断言值"
              prop="assertValue"
              align="center"
              :show-overflow-tooltip="true"
              :sortable="true"
            ></el-table-column>
            <el-table-column
              label="扩展参数"
              prop="extendArgvs"
              align="center"
              :show-overflow-tooltip="true"
              :sortable="true"
            ></el-table-column>
            <el-table-column
              label="步骤操作"
              prop="operation"
              align="center"
              class="col-report"
              :show-overflow-tooltip="true"
            >
              <template slot-scope="scope">
                <el-tooltip
                  class="item"
                  effect="light"
                  content="导入"
                  placement="top"
                  :hide-after="5000"
                  :enterable="false"
                >
                  <el-button
                    size="mini"
                    type="warning"
                    style="font-size: 10px"
                    round
                    icon="el-icon-circle-plus"
                    @click="onImportCaseStep(scope.row)"
                  ></el-button>
                </el-tooltip>
              </template>
            </el-table-column>
          </el-table>
          <template>
            <el-pagination
              @size-change="handleSizeChangeImport"
              @current-change="handleCurrentChangeImport"
              :page-sizes="[10, 20, 50, 100, 200, 400, 600, 1000, 10000]"
              :current-page="currentPageImport"
              :page-size="pageSizeImport"
              layout="total, sizes, prev, pager, next, jumper"
              :total="allStepTableData.length"
              :small="false"
              :background="true"
              :pager-count="6"
            ></el-pagination>
          </template>
        </el-dialog>
      </template>
      <template>
        <el-dialog
          :visible.sync="dialogTableVisible"
          :title="onStepTitle"
          class="table-dialog"
          :fullscreen="false"
          width="65%"
          style="text-align: center;"
        >
          <el-form
            :inline="true"
            :model="modifyResourceForm"
            :rules="modifyResourceRules"
            ref="modifyResourceForm"
            label-width="128px"
            size="mini"
            label-position="right"
          >
            <div class="form resource_form">
              <el-form-item label="用例名称" prop="casename" :required="true">
                <el-input
                  v-model="modifyResourceForm.casename"
                  placeholder="请输入中文（全局唯一）"
                  clearable
                  style="width: 258px;"
                ></el-input>
              </el-form-item>
              <el-form-item label="用例方法" :required="true" size="mini" prop="casefunc">
                <el-input
                  :disabled="true"
                  v-model="modifyResourceForm.casefunc"
                  placeholder="请输入英文（全局唯一，创建后不可更改只能删除）"
                  clearable
                  @blur="showPresentStep()"
                  style="width: 258px;"
                ></el-input>
              </el-form-item>
              <el-form-item label="用例类型" :required="true" prop="caseType" size="mini">
                <el-select
                  v-model="modifyResourceForm.caseType"
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
                  v-model="modifyResourceForm.caseEnv"
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
                  v-model="modifyResourceForm.caseRemark"
                  placeholder="请输入"
                  clearable
                  style="width: 258px;"
                ></el-input>
              </el-form-item>
            </div>
            <div class="form resource_form">
              <el-form-item label="动作方法" prop="eleAction" :required="true">
                <el-select
                  v-model="modifyResourceForm.eleAction"
                  clearable
                  filterable
                  size="mini"
                  no-data-text
                  @visible-change="collectElementAction()"
                  @change="valueRequired(value='action')"
                  class="argvForm"
                >
                  <el-option
                    v-for="item in modifyResourceForm.methodList"
                    :key="item"
                    :value="item"
                  ></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="动作描述" :required="true" size="mini" prop="actionDesc">
                <el-input
                  v-model="modifyResourceForm.actionDesc"
                  placeholder="请输入"
                  clearable
                  style="width: 258px;"
                ></el-input>
              </el-form-item>
              <el-form-item label="步骤顺序" :required="true" size="mini" prop="stepSequence">
                <el-select
                  clearable
                  style="width: 258px;"
                  v-model="modifyResourceForm.stepSequence"
                  size="mini"
                  filterable
                  :placeholder="stepMessage"
                  :disabled="stepAble"
                  @click="getStepsItem()"
                >
                  <el-option
                    v-for="item in stepOrder"
                    :key="item.order"
                    :label="item.desc"
                    :value="item.order"
                  ></el-option>
<!--                  <el-option-->
<!--                    v-for="item in options"-->
<!--                    :key="item.order"-->
<!--                    :label="item.desc"-->
<!--                    :value="item.order"-->
<!--                  ></el-option>-->
<!--                  <el-option-->
<!--                    v-for="(item) in 100"-->
<!--                    :key="item"-->
<!--                    :label="`第${item}步`"-->
<!--                    :value="item"-->
<!--                  ></el-option>-->
                </el-select>
              </el-form-item>
              <el-form-item label="定位方式" :required="false" size="mini" prop="locateType">
                <el-select
                  v-model="modifyResourceForm.locateType"
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
                  v-model="modifyResourceForm.locateValue"
                  placeholder="请输入"
                  clearable
                  style="width: 258px;"
                ></el-input>
              </el-form-item>
              <el-form-item label="动作参数" :required="actionRequired" size="mini" prop="actionValue">
                <el-input
                  v-model="modifyResourceForm.actionValue"
                  placeholder="请输入"
                  clearable
                  style="width: 258px;"
                ></el-input>
              </el-form-item>
              <el-form-item label="动作断言值" :required="false" size="mini" prop="assertValue">
                <el-input
                  v-model="modifyResourceForm.assertValue"
                  placeholder="请输入"
                  clearable
                  style="width: 258px;"
                ></el-input>
              </el-form-item>
              <el-form-item
                size="mini"
                v-for="(newArgv, index) in modifyResourceForm.argvs"
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
                  v-model="modifyResourceForm.remark"
                  placeholder="请输入"
                  clearable
                  style="width: 258px;"
                ></el-input>
              </el-form-item>
            </div>
            <el-form-item>
              <el-tooltip class="item" effect="dark" placement="top">
                <div slot="content">
                  提交数据
                  <br />
                </div>
                <el-button
                  type="danger"
                  @click="onSubmmitStepArgvs()"
                  round
                  icon="el-icon-edit"
                  style="display: inline"
                >{{buttonName}}</el-button>
              </el-tooltip>
              <el-tooltip class="item" effect="dark" placement="top">
                <div slot="content">
                  提交数据
                  <br />
                </div>
                <el-button
                  type="info"
                  @click="onSubmmitStepArgvs(dofunc=false)"
                  round
                  icon="el-icon-circle-close"
                >取消</el-button>
              </el-tooltip>
            </el-form-item>
          </el-form>
        </el-dialog>
      </template>
    </div>
  </div>
</template>

<script>
import headTop from '@/components/headTop'
import {
  showLoading,
  hideLoading,
  // stepOrder,
  pickerOptions
} from '@/config/common'
import {
  backendManageQueryCasename,
  backendManageQueryPresentStep,
  backendManageQueryCaseStep,
  backendManageUpdateStepForMove,
  backendManageAddStepThroughInsert,
  backendManageDelCaseStep,
  backendManageModifyStepArgvs,
  backendManageModifyCaseArgvs,
  backendQueryStepAccordDesc,
  deleteCaseAllSteps,
  backendManageGetCaseArgvs,
  getStepDict,
  backendManageQuerygroup,
  backendManageQueryenv
} from '@/api/getData'
export default {
  data () {
    return {
      return_env_list: [],
      return_list: [],
      stepOrder: [],
      pickerOptions,
      stepMessage: '请选择步骤',
      eleRequired: false,
      stepValue: '',
      actionRequired: false,
      resourceForm: {
        searchCaseList: [],
        timeRange: [],
        caseType: '',
        caseEnv: '',
        caseRemark: '',
        casename: ''
      },
      modifyResourceRules: {
        casename: [
          { required: true, message: '请输入用例名', trigger: 'blur' }
        ],
        casefunc: [
          { required: true, message: '请输入用例方法名', trigger: 'blur' }
        ],
        caseType: [
          { required: true, message: '请输入用例类型', trigger: 'blur' }
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
      importSearchForm: {
        actionDesc: '',
        descList: []
      },
      modifyResourceForm: {
        casefunc: '',
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
      },
      caseConfig: '',
      caseMap: {},
      argvsName: [],
      caseTableData: [],
      stepTableData: [],
      allStepTableData: [],
      dialogTableVisible: false,
      dialogStepTableVisible: false,
      dialogAllStepTableVisible: false,
      currentPage: 1,
      pageSize: 10,
      currentPageImport: 1,
      pageSizeImport: 10,
      queryLoading: false,
      buttonName: '',
      onStepTitle: '',
      importStepTitle: '',
      stepAble: false,
      caseInfoForImport: {}
    }
  },
  //   watch: {
  //     "resourceForm.env": {
  //       handler(newName, oldName) {
  //         const data = {
  //           env: this.resourceForm.env
  //         };
  //       }
  //     }
  //   },
  computed: {
    tableData: function () {
      return this.caseTableData.slice(
        (this.currentPage - 1) * this.pageSize,
        this.currentPage * this.pageSize
      )
    },
    importStepTableData: function () {
      return this.allStepTableData.slice(
        (this.currentPageImport - 1) * this.pageSizeImport,
        this.currentPageImport * this.pageSizeImport
      )
    }
    // options: function () {
    //   console.log(stepOrder())
    //   return stepOrder()
    // },
  },
  components: {
    headTop
  },
  mounted: function () {
    this.onQueryCasename()
  },
  created: function () {
    this.getGroupName()
    this.getStepsItem()
    this.getEnvName()
  },
  methods: {
    async getEnvName () {
      showLoading()
      try {
        const resp = await backendManageQueryenv({ 'IfAll': true })
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
    async getStepsItem () {
      showLoading()
      try {
        // const data = {}
        // 默认100个步骤达到上限（一条UI用例不推荐超过100个步骤）
        // data.num_instance = 100
        const resp = await getStepDict()
        // debugger;
        if (resp.code === 0) {
          this.stepOrder = resp.steps_list
        } else {
          this.stepOrder = []
        }
      } catch (err) {
        this.$message.error(err.message)
      } finally {
        // console.log(this.stepOrder)
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
          //   showClose: true,
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
    async queryStepAccordDesc () {
      try {
        const resp = await backendQueryStepAccordDesc({
          actionDesc: this.importSearchForm.actionDesc
        })
        this.allStepTableData = []
        if (resp.ResCode === 0) {
          resp.query_data.forEach((item, index) => {
            let data = {}
            data.casename = item.fields.case_name
            data.stepSequence = item.fields.step_seq
            data.eleAction = item.fields.ele_action
            data.actionDesc = item.fields.action_desc
            data.locateType = item.fields.loc_type
            data.locateValue = item.fields.loc_value
            data.actionValue = item.fields.action_value
            data.extendArgvs = item.fields.argvs_quotes_sd
            data.assertValue = item.fields.assert_value
            data.remark = item.fields.remark
            data.id = item.pk
            this.allStepTableData.push(data)
          })
        } else {
          this.$message.error(resp.ErrMsg)
        }
      } catch (err) {
        this.$message.error(err.message)
      }
    },
    onStepMove (index, row, up = true) {
      try {
        let temp = this.stepTableData[index - 1]
        this.$set(this.stepTableData, index - 1, this.stepTableData[index])
        this.$set(this.stepTableData, index, temp)
        this.moveFunc((index = index), (row = row), (up = up))
        this.$nextTick(() => {
          this.freshStepTableData((row = row))
          this.freshStepTableData((row = row))
        })
      } catch (err) {
        this.$message.error(err.message)
      }
    },
    async moveFunc (index, row, up) {
      try {
        var stepMove = []
        var data1 = {}
        var data2 = {}
        if (up) {
          data1.new_step_seq = row.stepSequence - 1
          data1.present_id = row.id
          data1.old_step_seq = row.stepSequence
          data1.case_func = row.casefunc
          data1.present = true
          stepMove.push(data1)
          data2.present = false
          data2.new_step_seq = row.stepSequence
          data2.old_step_seq = row.stepSequence - 1
          data2.case_func = row.casefunc
          stepMove.push(data2)
        } else {
          data1.new_step_seq = row.stepSequence + 1
          data1.present_id = row.id
          data1.old_step_seq = row.stepSequence
          data1.case_func = row.casefunc
          data1.present = true
          stepMove.push(data1)
          data2.present = false
          data2.new_step_seq = row.stepSequence
          data2.old_step_seq = row.stepSequence + 1
          data2.case_func = row.casefunc
          stepMove.push(data2)
        }
        const resp = await backendManageUpdateStepForMove({
          step_move: stepMove
        })
        if (resp.ResCode === 0) {
          if (up) {
            this.$message.success(`移动到第【${index}】步成功`)
          } else {
            this.$message.success(`移动到第【${index + 2}】步成功`)
          }
        } else {
          this.$message.error(resp.ErrMsg || '更新失败')
        }
      } catch (err) {
        this.$message.error(err.message)
      }
    },
    async freshStepTableData (row, queryAll = false) {
      try {
        if (queryAll === true) {
          var param = { query_type: 'all', case_func: row.casefunc }
          var resp = await backendManageQueryCaseStep(param)
          this.allStepTableData = []
        } else {
          var param = { case_func: row.casefunc }
          var resp = await backendManageQueryCaseStep(param)
          this.stepTableData = []
        }
        if (resp.ResCode === 0) {
          resp.case_step.forEach((item, index) => {
            let data = {}
            data.casefunc = row.casefunc
            data.casename = row.casename
            data.caseType = row.caseType
            data.caseEnv = row.caseEnv
            data.caseRemark = row.remark
            data.casename = item.fields.case_name
            data.stepSequence = item.fields.step_seq
            data.eleAction = item.fields.ele_action
            data.actionDesc = item.fields.action_desc
            data.locateType = item.fields.loc_type
            data.locateValue = item.fields.loc_value
            data.actionValue = item.fields.action_value
            data.extendArgvs = item.fields.argvs_quotes_sd
            data.assertValue = item.fields.assert_value
            data.remark = item.fields.remark
            data.id = item.pk
            if (queryAll === true) {
              this.allStepTableData.push(data)
            } else {
              this.stepTableData.push(data)
            }
          })
        } else {
          this.$notify.error(resp.ErrMsg)
          return
        }
      } catch (err) {
        this.$message.error(err.message)
      }
    },
    async generatorDescList () {
      try {
        const param = { query_type: 'all' }
        const resp = await backendManageQueryCaseStep(param)
        this.importSearchForm.descList = []
        if (resp.ResCode === 0) {
          resp.case_step.forEach((item, index) => {
            let data = {}
            data.key = index + 1
            data.value = item.fields.action_desc
            this.importSearchForm.descList.push(data)
          })
        } else {
          this.$notify.error(resp.ErrMsg)
        }
      } catch (err) {
        this.$message.error(err.message)
      }
    },
    paramAddFunc () {
      this.$router.push('backParamAdd')
    },
    onEditStepArgvs (row) {
      try {
        this.buttonName = '修改'
        this.stepAble = true
        this.caseConfig = row.casename
        this.stepValue = row.stepSequence
        this.onStepTitle = `【${this.caseConfig}】**第【${this.stepValue}】步**参数修改`
        this.generateArgvsList(row)
        this.dialogTableVisible = true
      } catch (err) {
        this.$message({
          type: 'error',
          message: err.message
        })
      }
    },
    onNewStepArgvs (index, row) {
      try {
        this.buttonName = '新增'
        this.stepAble = false
        this.caseConfig = row.casename
        this.stepValue = row.stepSequence
        this.onStepTitle = `【${this.caseConfig}】**插入第【${this.stepValue}】步**参数（插入新增）`
        this.generateArgvsList(row)
        this.dialogTableVisible = true
      } catch (err) {
        this.$message({
          type: 'error',
          message: err.message
        })
      }
    },
    onShowStepArgvs (row) {
      try {
        this.caseConfig = row.casename
        this.freshStepTableData((row = row))
        this.dialogStepTableVisible = true
      } catch (err) {
        this.$message({
          type: 'error',
          message: err.message
        })
      }
    },
    async onQueryForImport (row, queryAll = true) {
      try {
        this.caseInfoForImport = {}
        this.caseInfoForImport.casefunc = row.casefunc
        this.caseInfoForImport.stepSequence = row.stepSequence
        this.caseInfoForImport.caseType = row.caseType
        this.caseInfoForImport.caseEnv = row.caseEnv
        this.caseInfoForImport.casename = this.caseConfig = row.casename
        this.freshStepTableData((row = row), (queryAll = queryAll))
        this.importStepTitle = `导入数据作为用例【${row.casename}】的第【${row.stepSequence}】个步骤`
        this.dialogAllStepTableVisible = true
      } catch (err) {
        this.$message({
          type: 'error',
          message: err.message
        })
      }
    },
    async onImportCaseStep (row) {
      try {
        const param = {
          casename: this.caseInfoForImport.casename,
          case_func: this.caseInfoForImport.casefunc,
          action_desc: row.actionDesc,
          ele_action: row.eleAction,
          locate_type: row.locateType,
          step_seq: this.caseInfoForImport.stepSequence,
          locate_value: row.locateValue,
          action_value: row.actionValue,
          assert_value: row.assertValue,
          remark: row.remark,
          argvs: row.argvs
        }
        const resp = await backendManageAddStepThroughInsert(param)
        if (resp.ResCode === 0) {
          this.$message.success('导入成功...')
          this.freshStepTableData((row = this.caseInfoForImport))
        } else {
          this.$message.error(resp.ErrMsg || '导入失败...')
        }
      } catch (err) {
        this.$message.error(err.message)
      }
    },
    async showPresentStep () {
      try {
        const resp = await backendManageQueryPresentStep({
          case_func: this.modifyResourceForm.casefunc
        })
        if (resp.ResCode === 0) {
          if (resp.step_count) {
            this.stepMessage = `当前用例已经存在【${resp.step_count}】步配置信息`
          }
        } else {
          this.$message.error(resp.ErrMsg)
        }
      } catch (err) {
        this.$message.error(err.message)
      }
    },
    async valueRequired (value = 'element') {
      try {
        const resp = await backendManageGetCaseArgvs({
          funcname: 'generatorArgvsList'
        })
        if (resp.ResCode === 0) {
          this.argvsPost = []
          const extend_argvs =
            resp.argvs[this.modifyResourceForm.eleAction] || []
          if (extend_argvs.length !== 0) {
            this.argvsPost = extend_argvs
            this.argvsPost.forEach((item, index) => {
              let data = {}
              data.name = item
              this.modifyResourceForm.argvs.push(data)
            })
          }
        } else {
          this.$message({
            type: 'error',
            message: resp.ErrMsg,
            center: true
          })
        }
        if (value === 'element') {
          this.eleRequired = !!this.modifyResourceForm.locateType
        } else {
          this.actionRequired =
            this.modifyResourceForm.eleAction === 'input'
        }
      } catch (err) {
        this.$message.error(err.message)
      }
    },
    async collectElementAction () {
      try {
        const resp = await backendManageGetCaseArgvs({
          funcname: 'collectElementAction'
        })
        if (resp.ResCode === 0) {
          this.modifyResourceForm.methodList = []
          this.modifyResourceForm.methodList = resp.operation_method
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
    generateArgvsList (row) {
      try {
        const argvsObject = JSON.parse(row.extendArgvs)
        this.argvsName = Object.keys(argvsObject)
        this.modifyResourceForm.argvs = []
        this.argvsName.forEach((item, index) => {
          let data = {}
          data.name = item
          data.value = argvsObject[this.argvsName[index]]
          this.modifyResourceForm.argvs.push(data)
        })
        // this.modifyResourceForm = { ...row, ...this.modifyResourceForm };
        this.modifyResourceForm.casename = row.casename
        this.modifyResourceForm.casefunc = row.casefunc
        this.modifyResourceForm.caseType = row.caseType
        this.modifyResourceForm.caseEnv = row.caseEnv
        this.modifyResourceForm.caseRemark = row.caseRemark
        this.modifyResourceForm.eleAction = row.eleAction
        this.modifyResourceForm.actionDesc = row.actionDesc
        this.modifyResourceForm.stepSequence = row.stepSequence
        this.modifyResourceForm.actionValue = row.actionValue
        this.modifyResourceForm.locateType = row.locateType
        this.modifyResourceForm.locateValue = row.locateValue
        this.modifyResourceForm.assertValue = row.assertValue
        this.modifyResourceForm.remark = row.remark
      } catch (err) {
        this.$message.error(err.message)
      }
    },
    resourceMessageBox (index, row, delCase = false) {
      this.$confirm('此操作将永久删除该项, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          this.deleteCaseParam(index, row, (delCase = delCase))
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          })
        })
    },
    async deleteCaseParam (index, row, delCase) {
      try {
        var param = {
          index: index,
          case_func: row.casefunc,
          case_name: row.casename
        }
        this.$message({
          type: 'info',
          center: true,
          duration: 6000,
          message:
            '亲，正在备份数据，稍后执行删除操作，请等待删除成功提示。。。'
        })
        if (delCase === true) {
          const resp = await deleteCaseAllSteps(param)
          this.tableData.splice(index, 1)
          if (resp.ResCode === 0) {
            this.onQueryCasename()
            this.$message.success('删除用例及其步骤成功')
          } else {
            throw new Error(resp.ErrMsg)
          }
        } else {
          const resp = await backendManageDelCaseStep(param)
          this.stepTableData.splice(index, 1)
          if (resp.ResCode === 0) {
            this.freshStepTableData((row = row))
            this.$message({
              type: 'success',
              message: '删除成功',
              center: true
            })
          } else {
            throw new Error(resp.ErrMsg)
          }
        }
      } catch (err) {
        this.$message({
          type: 'error',
          message: err.message
        })
      }
    },
    resetForm () {
      this.$refs.resourceForm.resetFields()
      this.$message({
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
    handleSizeChangeImport (val) {
      // console.log(`每页 ${val} 条`);
      showLoading()
      this.pageSizeImport = val
      hideLoading()
    },
    handleCurrentChangeImport (val) {
      showLoading()
      this.currentPageImport = val
      // console.log(`当前页: ${val}`);
      hideLoading()
    },
    async onSubmmitStepArgvs (dofunc = true) {
      if (dofunc) {
        this.$refs.modifyResourceForm.validate(async valid => {
          try {
            if (valid) {
              const argvsObject = this.argvsName.reduce((p, c, i) => {
                p[c] = this.modifyResourceForm.argvs[i].value
                return p
              }, {})
              const param = {
                casename: this.modifyResourceForm.casename,
                case_func: this.modifyResourceForm.casefunc,
                case_type: this.modifyResourceForm.caseType,
                case_env: this.modifyResourceForm.caseEnv,
                caseRemark: this.modifyResourceForm.caseRemark,
                action_desc: this.modifyResourceForm.actionDesc,
                ele_action: this.modifyResourceForm.eleAction,
                locate_type: this.modifyResourceForm.locateType,
                step_seq: this.modifyResourceForm.stepSequence,
                locate_value: this.modifyResourceForm.locateValue,
                action_value: this.modifyResourceForm.actionValue,
                assert_value: this.modifyResourceForm.assertValue,
                remark: this.modifyResourceForm.remark,
                argvs: argvsObject
              }
              // console.log(param);
              this.$message.info({
                message: '开始写入数据...',
                center: true
              })
              if (this.buttonName === '修改') {
                const resp_data = await backendManageModifyStepArgvs(param)
                if (resp_data.ResCode === 0) {
                  var resp = await backendManageModifyCaseArgvs(param)
                } else {
                  this.$message.error(resp_data.ErrMsg)
                  return
                }
              } else {
                var resp = await backendManageAddStepThroughInsert(param)
              }
              if (resp.ResCode === 0) {
                let presentRow = {}
                presentRow.casefunc = this.modifyResourceForm.casefunc
                presentRow.caseType = this.modifyResourceForm.caseType
                presentRow.caseEnv = this.modifyResourceForm.caseEnv
                presentRow.caseRemark = this.modifyResourceForm.remark
                try {
                  this.freshStepTableData(presentRow)
                  this.onQueryCasename()
                  this.$message.success({ message: '操作成功!', center: true })
                } catch (err) {
                  this.$message.error(err.message)
                  return
                }
              } else {
                this.$notify.error({
                  message: resp.ErrMsg || '操作失败！',
                  center: true
                })
              }
            } else {
              this.$notify.error({
                title: 'ERROR',
                message: '亲，必填项不能为空哟...',
                center: true,
                offset: 288
              })
            }
          } catch (err) {
            this.$message.error(err.message)
          }
        })
      } else {
        this.dialogTableVisible = false
        this.$message.info({ message: '操作已取消！', center: true })
      }
    },
    async onQuerySingleCaselist () {
      showLoading()
      this.queryLoading = true
      try {
        const param = {
          single: false
        }
        const resp = await backendManageQueryCasename(param)
        this.resourceForm.searchCaseList = []
        if (resp.ResCode === 0) {
          resp.query_case_data.forEach((item, index) => {
            const data = {}
            data.casename = item.fields.case_name
            data.casefunc = item.fields.case_func
            this.resourceForm.searchCaseList.push(data)
          })
        } else {
          this.$message.error(resp.ErrMsg || '查询失败...')
        }
      } catch (err) {
        this.$message({
          type: 'error',
          message: err.message
        })
      } finally {
        this.queryLoading = false
        hideLoading()
      }
    },
    async onQueryCasename () {
      showLoading()
      this.queryLoading = true
      try {
        var timeRange = this.resourceForm.timeRange
        let timeInstance = ['2000-01-01 00:00:00', '3000-01-01 00:00:00']
        timeRange = timeRange != null ? timeRange : timeInstance
        timeRange = timeRange.length > 0 ? timeRange : timeInstance
        const param = {
          case_func: this.resourceForm.casename,
          case_type: this.resourceForm.caseType,
          case_env: this.resourceForm.caseEnv,
          remark: this.resourceForm.caseRemark,
          start_time: timeRange[0],
          end_time: timeRange[1]
        }
        const resp = await backendManageQueryCasename(param)
        this.caseTableData = []
        if (resp.ResCode === 0) {
          resp.query_case_data.forEach((item, index) => {
            const data = {}
            const operation = {}
            data.casename = item.fields.case_name
            data.casefunc = item.fields.case_func
            data.caseType = item.fields.case_type
            data.caseEnv = item.fields.case_env
            data.remark = item.fields.remark
            data.createTime = item.fields.create_time
            operation.key = ''
            data.operation = operation
            data.number = index + 1
            this.caseTableData.push(data)
          })
          if (this.caseTableData.length === 0) {
            this.caseTableData = []
          }
          this.$message({
            type: 'success',
            message:
              '查询成功, 共计 ' + this.caseTableData.length + ' 条结果...'
          })
        } else {
          this.$message.error(resp.ErrMsg || '查询失败...')
        }
      } catch (err) {
        this.$message({
          type: 'error',
          message: err.message
        })
      } finally {
        this.queryLoading = false
        hideLoading()
      }
    }
  }
}
</script>

<style lang="less" scoped>
@import "../style/mixin";
.param_table {
  padding: 0% 2% 0% 1%;
}
.resource_table {
  max-height: 100%;
  width: 100%;
}
.step_resource_table {
  max-height: 100%;
  width: 100%;
}
.col-report {
  background-color: rgba(2, 17, 3, 0.788);
}
.form {
  min-width: 90%;
  margin-bottom: 20px;
  // text-align: center;
  &:hover {
    box-shadow: 0 0 8px 0 rgba(232, 237, 250, 0.6),
      0 2px 4px 0 rgba(232, 237, 250, 0.5);
    border-radius: 6px;
    transition: all 400ms;
  }
}
.resource_form {
  border: 1px solid #eaeefb;
  padding: 3% 1% 1% 1%;
}
.argvForm {
  width: 258px;
}
.table-dialog {
  background: #c1c9e0;
}
</style>
