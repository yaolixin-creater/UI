import fetch from '@/config/fetch'

/**
 * 退出
 */

export const signout = () => fetch('/user/signout')

/**
 * 用户注册
 */

export const register = data => fetch('/user/register', data, 'POST')

/**
 * login
 */

export const login = data => fetch('/user/login', data, 'POST')

/**
 * send email verification code
 */

export const sendEmailCode = data => fetch('/user/sendEmailCode', data, 'POST')

/**
 * modify password
 */

export const modifyPassword = data => fetch('/user/modifyPassword', data, 'POST')

/**
 * query back-end management case name from db
 */

export const backendManageQueryCasename = data => fetch('/backendManage/queryCasename', data, 'POST')

/**
 * get back-end management case argvs of extending from operation_map
 */

export const backendManageGetCaseArgvs = data => fetch('/backendManage/getCaseArgvs', data, 'POST')

/**
 * get back-end management case argvs into db
 */

export const backendManageAddCaseArgvs = data => fetch('/backendManage/addCaseArgvs', data, 'POST')

/**
 * add back-end management step argvs into db
 */

export const backendManageAddStepArgvs = data => fetch('/backendManage/addStepArgvs', data, 'POST')

/**
 * queryPresentStep
 */

export const backendManageQueryPresentStep = data => fetch('/backendManage/queryPresentStep', data, 'POST')

/**
 * queryCaseStep
 */

export const backendManageQueryCaseStep = data => fetch('/backendManage/queryCaseStep', data, 'POST')

/**
 * queryCaseStep
 */

export const backendManageUpdateStepForMove = data => fetch('/backendManage/updateStepForMove', data, 'POST')

/**
 * add case step through insert method
 */

export const backendManageAddStepThroughInsert = data => fetch('/backendManage/addStepThroughInsert', data, 'POST')

/**
 * del case step
 */

export const backendManageDelCaseStep = data => fetch('/backendManage/delCaseStep', data, 'POST')

/**
 * del case step
 */

export const backendManageModifyStepArgvs = data => fetch('/backendManage/modifyStepArgvs', data, 'POST')

/**
 *  modify case argvs
 */

export const backendManageModifyCaseArgvs = data => fetch('/backendManage/modifyCaseArgvs', data, 'POST')

/**
 *  modify case argvs
 */

export const backendManageRunTest = data => fetch('/backendManage/runTest', data, 'POST')

/**
 * 获取测试报告
 */

export const backendManageGetReport = report_name => fetch('/backendManage/getReport/', report_name, 'true')

/**
 *  查询所有测试报告
 */

export const backendManageQueryReport = data => fetch('/backendManage/queryReport', data, 'POST')

/**
 *  查询测试条目
 */

export const backendManageQuerySummary = data => fetch('/backendManage/querySummary', data, 'POST')

/**
 *  查询测试条目
 */

export const backendManageQueryCaseTested = data => fetch('/backendManage/queryCaseTested', data, 'POST')

/**
 *  查询登陆详情
 */

export const getLoginResult = data => fetch('/backendManage/getLoginResult', data, 'POST')

/**
 *  重置登陆详情
 */

export const initLoginResult = data => fetch('/backendManage/initLoginResult', data, 'POST')

/**
 *  删除用例以及用例所有步骤
 */

export const deleteCaseAllSteps = data => fetch('/backendManage/deleteCaseAllSteps', data, 'POST')

/**
 *  根据分组查询测试用例
 */

export const queryGroupCase = data => fetch('/backendManage/queryGroupCase', data, 'POST')

/**
 *  根据分组查询测试用例
 */

export const backendQueryStepAccordDesc = data => fetch('/backendManage/queryStepAccordDesc', data, 'POST')

/**
 *  删除测试报告
 */

export const backendManageDelReport = data => fetch('/backendManage/delReport', data, 'POST')

/**
 *  修改步骤的点位元素值
 */

export const modifysteps = data => fetch('/backendManage/modifysteps', data, 'POST')

/**
 *  查询分组
 */

export const backendManageQuerygroup = data => fetch('/backendManage/show_groups', data, 'POST')

/**
 *  删除分组
 */

export const backendManageDelgroup = data => fetch('/backendManage/del_group_name', data, 'POST')

/**
 *  查询分组详情
 */

export const backendManageQuerygroups = data => fetch('/backendManage/show_groups_details', data, 'POST')

/**
 *  创建分组
 */

export const backendManagecreategroup = data => fetch('/backendManage/create_group', data, 'POST')

/**
 *  修改分组
 */

export const backendManagemodgroup = data => fetch('/backendManage/mod_group_name', data, 'POST')

/**
 *  动态获取步骤配置
 */

export const getStepDict = data => fetch('/backendManage/getStepDict', data, 'POST')

/**
 *  查询环境
 */

export const backendManageQueryenv = data => fetch('/backendManage/show_envs', data, 'POST')

/**
 *  删除环境
 */

export const backendManageDelenv = data => fetch('/backendManage/del_env_name', data, 'POST')

/**
 *  查询环境详情
 */

export const backendManageQueryenvs = data => fetch('/backendManage/show_envs_details', data, 'POST')

/**
 *  创建环境
 */

export const backendManagecreateenv = data => fetch('/backendManage/create_env', data, 'POST')

/**
 *  修改环境
 */

export const backendManagemodenv = data => fetch('/backendManage/mod_env_name', data, 'POST')
