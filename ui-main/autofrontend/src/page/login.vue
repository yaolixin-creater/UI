<template>
  <div class="login_page fillcontain">
    <transition name="form-fade" mode="in-out">
      <section class="form_contianer" v-show="showLogin">
        <div class="manage_tip">
          <p>UI TEST PLATFORM</p>
        </div>
        <el-form :model="loginForm" :rules="rules" ref="loginForm">
          <el-form-item prop="username">
            <el-input v-model="loginForm.username" placeholder="用户名" clearable></el-input>
          </el-form-item>
          <el-form-item prop="password">
            <el-input
              type="password"
              placeholder="密码"
              v-model="loginForm.password"
              clearable
              show-password
              maxlength="24"
            ></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitLoginForm('loginForm')" class="submit_btn">登陆</el-button>
          </el-form-item>
          <el-checkbox v-model="passwordChecked" size="mini">
            <p style="font-size: 12px">记住密码</p>
          </el-checkbox>
        </el-form>
        <p>
          <span class="tip">温馨提示：</span>
          <el-button type="text" @click="dialogTableVisible=true" size="mini">点击注册!</el-button>
          <el-button @click="forgetDialogTableVisible=true" type="text" size="mini">忘记密码?</el-button>
        </p>
        <template>
          <el-dialog
            title="密码修改"
            :visible.sync="forgetDialogTableVisible"
            class="dialog"
            :fullscreen="false"
            style="text-align: center;"
          >
            <el-form
              :model="forgetForm"
              :rules="forgetRules"
              ref="forgetForm"
              label-width="100px"
              size="mini"
              class="form info_form"
            >
              <el-form-item label="新密码" prop="password" :required="true">
                <el-tooltip class="item" effect="dark" placement="right" hide-after="3000">
                  <div slot="content">
                    密码长度为8到24位;
                    <br />并且包含大小写字母和数字
                  </div>
                  <el-input
                    v-model="forgetForm.password"
                    clearable
                    size="mini"
                    type="password"
                    show-password
                  ></el-input>
                </el-tooltip>
              </el-form-item>
              <el-form-item label="确认密码" prop="passwordConfirm" :required="true">
                <el-tooltip class="item" effect="dark" placement="right" hide-after="3000">
                  <div slot="content">
                    密码长度为8到24位;
                    <br />并且包含大小写字母和数字
                  </div>
                  <el-input
                    show-password
                    v-model="forgetForm.passwordConfirm"
                    clearable
                    size="mini"
                    type="password"
                  ></el-input>
                </el-tooltip>
              </el-form-item>
              <el-form-item label="邮箱" prop="email" :required="true">
                <el-tooltip class="item" effect="dark" placement="right" hide-after="3000">
                  <div slot="content">请填写合法有效的163邮箱邮箱号</div>
                  <el-input v-model="forgetForm.email" clearable size="mini"></el-input>
                </el-tooltip>
              </el-form-item>
              <el-form-item :required="true" clearable prop="code">
                <el-col :span="10">
                  <el-button
                    type="text"
                    @click="sendVerificationCode(formName='forgetForm')"
                    size="mini"
                  >
                    <p>获取邮箱验证码</p>
                  </el-button>
                </el-col>
                <el-col :span="10">
                  <el-input
                    v-model="forgetForm.code"
                    clearable
                    size="mini"
                    v-if="codeVisible"
                    placeholder="请输入邮箱验证码"
                    style
                  ></el-input>
                </el-col>
              </el-form-item>
              <el-form-item style="margin-right: 118px">
                <el-button
                  type="success"
                  @click="submitForgetForm('forgetForm')"
                  icon="el-icon-edit"
                  round
                >修改</el-button>
                <el-button
                  round
                  type="danger"
                  icon="el-icon-warning"
                  @click="reset('forgetForm')"
                  style
                >重置</el-button>
              </el-form-item>
            </el-form>
          </el-dialog>
        </template>
        <template>
          <el-dialog
            title="新用户注册"
            :visible.sync="dialogTableVisible"
            class="dialog"
            :fullscreen="false"
            style="text-align: center;"
          >
            <el-form
              :model="registerForm"
              :rules="registerRules"
              ref="registerForm"
              label-width="100px"
              class="form info_form"
              :inline-message="false"
            >
              <el-form-item label="用户名" prop="username" :required="true">
                <el-input v-model="registerForm.username" clearable size="mini"></el-input>
              </el-form-item>
              <el-form-item label="密码" prop="password" :required="true">
                <el-tooltip class="item" effect="dark" placement="right" hide-after="3000">
                  <div slot="content">
                    密码长度为8到24位;
                    <br />并且包含大小写字母和数字
                  </div>
                  <el-input
                    v-model="registerForm.password"
                    clearable
                    size="mini"
                    type="password"
                    show-password
                  ></el-input>
                </el-tooltip>
              </el-form-item>
              <el-form-item label="确认密码" prop="passwordConfirm" :required="true">
                <el-tooltip class="item" effect="dark" placement="right" hide-after="3000">
                  <div slot="content">
                    密码长度为8到24位;
                    <br />并且包含大小写字母和数字
                  </div>
                  <el-input
                    show-password
                    v-model="registerForm.passwordConfirm"
                    clearable
                    size="mini"
                    type="password"
                  ></el-input>
                </el-tooltip>
              </el-form-item>
              <el-form-item label="性别" prop="gender">
                <el-select v-model="registerForm.gender" style="width:100%;" clearable size="mini">
                  <el-option
                    v-for="item in genderList"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                  ></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="电话" prop="cellphone" :required="true">
                <el-input v-model="registerForm.cellphone" clearable size="mini"></el-input>
              </el-form-item>
              <el-form-item label="介绍" prop="description">
                <el-input v-model="registerForm.description" clearable size="mini"></el-input>
              </el-form-item>
              <el-form-item label="邮箱" prop="email" :required="true">
                <el-tooltip class="item" effect="dark" placement="right" hide-after="3000">
                  <el-input v-model="registerForm.email" clearable size="mini"></el-input>
                </el-tooltip>
              </el-form-item>
              <el-form-item :required="true" clearable prop="code">
                <el-col :span="10">
                  <el-button type="text" @click="sendVerificationCode()" size="mini">
                    <p>获取邮箱验证码</p>
                  </el-button>
                </el-col>
                <el-col :span="10">
                  <el-input
                    v-model="registerForm.code"
                    clearable
                    size="mini"
                    v-if="codeVisible"
                    placeholder="请输入邮箱验证码"
                    style
                  ></el-input>
                </el-col>
              </el-form-item>
              <el-form-item label-width="10px">
                <el-upload
                  class="avatar-uploader"
                  :action="baseUrl + '/user/uploadImage'"
                  :show-file-list="true"
                  :on-success="uploadImg"
                  :before-upload="beforeImgUpload"
                  name="headPortrait"
                  drag
                  accept=".jpg, .jpeg, .png, .gif, .bmp, .pdf, .JPG, .JPEG, .PBG, .GIF, .BMP, .PDF"
                  multiple
                  :limit="1"
                  :auto-upload="true"
                >
                  <img
                    v-if="registerForm.image_path"
                    :src="baseImgPath + registerForm.image_path"
                    class="avatar"
                  />
                  <i v-else class="el-icon-plus avatar-uploader-icon"></i>
                  <i class="el-icon-upload"></i>
                  <div class="el-upload__text">
                    将头像文件拖到此处，或
                    <em>点击上传</em>
                  </div>
                  <div slot="tip" class="el-upload__tip">只能上传图片,且不超过2MB</div>
                </el-upload>
              </el-form-item>
              <el-form-item style="margin-right: 118px">
                <el-button
                  type="success"
                  @click="submitRegisterForm('registerForm')"
                  icon="el-icon-edit"
                  round
                  size="mini"
                >注册</el-button>
                <el-button
                  style
                  round
                  size="mini"
                  type="danger"
                  icon="el-icon-warning"
                  @click="reset('registerForm')"
                >重置</el-button>
              </el-form-item>
            </el-form>
          </el-dialog>
        </template>
      </section>
    </transition>
  </div>
</template>

<script>
import { login, register, sendEmailCode, modifyPassword } from '@/api/getData'
import { mapState } from 'vuex'
import { baseUrl, baseImgPath } from '@/config/env'
import { clearToken } from '@/config/common'
export default {
  data () {
    return {
      baseUrl,
      baseImgPath,
      codeVisible: false,
      passwordChecked: true,
      uuid: '',
      imageData: {},
      backendEmailCode: '',
      forgetDialogTableVisible: false,
      dialogTableVisible: false,
      forgetForm: {
        email: '',
        code: '',
        password: '',
        passwordConfirm: ''
      },
      forgetRules: {
        email: [{ required: true, message: '请输入邮箱名', trigger: 'blur' }],
        password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
        code: [{ required: true, message: '验证码为必填项', trigger: 'blur' }],
        passwordConfirm: [
          { required: true, message: '请输入确认密码', trigger: 'blur' }
        ]
      },
      registerForm: {
        genderList: [],
        gender: '',
        password: '',
        passwordConfirm: '',
        username: '',
        description: '',
        email: '',
        cellphone: '',
        code: '',
        firstEmail: ''
      },
      genderList: [
        {
          value: '男',
          label: '男'
        },
        { value: '女', label: '女' }
      ],
      registerRules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        email: [{ required: true, message: '请输入邮箱名', trigger: 'blur' }],
        password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
        code: [{ required: true, message: '验证码为必填项', trigger: 'blur' }],
        cellphone: [
          { required: true, message: '手机号为必填项', trigger: 'blur' }
        ],
        passwordConfirm: [
          { required: true, message: '请输入确认密码', trigger: 'blur' }
        ]
      },
      loginForm: {
        username: '',
        password: ''
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
      },
      showLogin: false
    }
  },
  mounted () {
    this.showLogin = true
    this.getlocalStorage()
  },
  computed: {
    ...mapState(['adminInfo'])
  },
  methods: {
    reset (formName) {
      this.$refs[formName].resetFields()
      this.$message({
        type: 'success',
        message: '已清除'
      })
    },
    verifyEmail (email) {
      var reg = /^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/
      if (!reg.test(email)) {
        this.$message.error('请输入有效的邮箱')
        return false
      }
      // if (email.indexOf('163') < 0) {
      //   this.$message.error('请使用邮箱号163')
      //   return false
      // }
    },
    async sendVerificationCode (formName = 'registerForm') {
      try {
        if (formName === 'registerForm') {
          var email = this.registerForm.email
        } else if (formName === 'forgetForm') {
          var email = this.forgetForm.email
        } else {
          return false
        }
        if (email === '') {
          this.$message.error('未填写邮箱')
          return
        } else {
          if (this.verifyEmail(email) === false) {
            return
          }
        }
        this.codeVisible = true
        const param = { email: email }
        this.$message.success('验证码已发送')
        const resp = await sendEmailCode(param)
        if (resp.ResCode === 0) {
          this.backendEmailCode = resp.email_code
          this.$message.success('邮箱验证码发送成功, 请查收')
          this.firstEmail = email
        } else {
          this.$message.error(resp.ErrMsg)
        }
      } catch (err) {
        this.$message.error(err.message)
      }
    },
    guid () {
      function S4 () {
        return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1)
      }
      return (
        S4() +
        S4() +
        '-' +
        S4() +
        '-' +
        S4() +
        '-' +
        S4() +
        '-' +
        S4() +
        S4() +
        S4()
      )
    },
    uploadImg (res, file) {
      if (res.ResCode === 0) {
        this.registerForm.image_path = res.image_path
        this.$message.success('上传图片成功！')
        this.imageData = {
          image_path: res.image_path,
          image_name: file.name,
          image_size: file.size
        }
      } else {
        this.$message.error('上传图片失败！')
      }
    },
    beforeImgUpload (file) {
      const isRightType =
        file.type === 'image/jpeg' || file.type === 'image/png'
      const isLt2M = file.size / 1024 / 1024 < 2
      if (!isRightType) {
        this.$message.error('上传头像图片只能是JPG, PNG, JPEG格式!')
      }
      if (!isLt2M) {
        this.$message.error('上传头像图片大小不能超过 2MB!')
      }
      return isRightType && isLt2M
    },
    setlocalStorage (username, password) {
      localStorage.autoUsernameForRemember = username
      localStorage.autoPasswordForRemember = password
    },
    getlocalStorage: function () {
      this.loginForm.username = localStorage.getItem('autoUsernameForRemember')
      this.loginForm.password = localStorage.getItem('autoPasswordForRemember')
    },
    async submitLoginForm (formName) {
      this.$refs[formName].validate(async valid => {
        try {
          if (valid) {
            const res = await login({
              username: this.loginForm.username,
              password: this.loginForm.password
            })
            if (res.ResCode === 0) {
              if (res.login_code === 0) {
                this.$message({
                  showClose: true,
                  type: 'success',
                  message: '登录成功'
                })
                if (this.passwordChecked === true) {
                  this.setlocalStorage(
                    this.loginForm.username,
                    this.loginForm.password
                  )
                } else {
                  this.setlocalStorage('', '')
                }
                if (res.user_token) {
                  var user_token = res.user_token
                  if (user_token !== '') {
                    localStorage.autoTokenForVerify = user_token
                  }
                }
                this.$router.push('home')
                // this.$router.go(-1);
              } else {
                clearToken()
                if (this.passwordChecked === true) {
                  this.setlocalStorage(
                    this.loginForm.username,
                    this.loginForm.password
                  )
                } else {
                  this.setlocalStorage('', '')
                }
                if (res.login_code === 1) {
                  this.$message.error('密码错误')
                } else if (res.login_code === 2) {
                  this.$message.error('用户不存在')
                } else if (res.login_code === 3) {
                  this.$message.error(res.user_login_err)
                }
              }
            } else {
              this.$message({
                type: 'error',
                message: res.ErrMsg || '登陆失败。。。'
              })
            }
          } else {
            this.$notify.error({
              title: 'ERROR',
              message: '用户名与密码不可为空',
              offset: 288,
              center: true
            })
          }
        } catch (err) {
          this.$message.error(err.message)
        }
      })
    },
    passwordValid (valPwd) {
      if (
        valPwd == null ||
        valPwd.length < 8 ||
        valPwd.length > 24 ||
        valPwd.trim().length === ''
      ) {
        this.$message.error('密码长度为8到24位')
        return false
      }
      let arrVerify = [
        { regName: 'Number', regValue: /^.*[0-9]+.*/ },
        { regName: 'LowerCase', regValue: /^.*[a-z]+.*/ },
        { regName: 'UpperCase', regValue: /^.*[A-Z]+.*/ },
        { regName: 'SpecialCharacters', regValue: /^.*[^a-zA-Z0-9]+.*/ }
      ]
      let regNum = 0 // 记录匹配的次数
      for (let iReg = 0; iReg < arrVerify.length; iReg++) {
        if (arrVerify[iReg].regValue.test(valPwd)) {
          regNum = regNum + 1
        }
      }
      if (regNum <= 2) {
        this.$message.error('密码必须包含大小写字母和数字')
        return false
      }
    },
    async submitRegisterForm (formName) {
      try {
        this.uuid = this.guid()
        this.$set(this.imageData, 'uuid', this.uuid)
        this.$refs[formName].validate(async valid => {
          if (valid) {
            var reg = /^1[3456789]\d{9}$/
            if (this.registerForm.cellphone) {
              if (!reg.test(this.registerForm.cellphone)) {
                this.$message.error('请输入有效的手机号码')
                return
              }
            }
            if (this.backendEmailCode !== this.registerForm.code) {
              this.$message.error('验证码错误，请重新获取!')
              return
            }
            if (
              this.registerForm.password !== this.registerForm.passwordConfirm
            ) {
              this.$message.error('两次输入密码不一致，请重新输入')
              return
            }
            if (this.passwordValid(this.registerForm.password) === false) {
              return
            }
            if (this.verifyEmail(this.registerForm.email) === false) {
              return
            }
            if (this.firstEmail !== this.registerForm.email) {
              this.$message.error('您输入的邮箱与获取验证码的邮箱不一致！')
              return
            }
            const param = {
              username: this.registerForm.username,
              password: this.registerForm.password,
              passwordConfirm: this.registerForm.passwordConfirm,
              gender: this.registerForm.gender,
              email: this.registerForm.email,
              fronted_email_code: this.registerForm.code,
              cellphone: this.registerForm.cellphone,
              description: this.registerForm.description,
              ...this.imageData
            }
            const res = await register(param)
            this.uuid = ''
            if (res.ResCode === 0) {
              this.$message({
                type: 'success',
                message: '注册成功'
              })
              this.dialogTableVisible = false
            } else {
              this.$message({
                type: 'error',
                message: res.ErrMsg
              })
            }
          } else {
            this.$notify.error({
              title: 'ERROR',
              message: '亲，必填项不能为空哟',
              offset: 288
            })
          }
        })
      } catch (err) {
        this.$message.error(err.message)
      }
    },
    async submitForgetForm (formName) {
      this.$refs[formName].validate(async valid => {
        try {
          if (valid) {
            if (this.backendEmailCode !== this.forgetForm.code) {
              this.$message.error('验证码错误，请重新获取')
              return
            }
            if (this.forgetForm.password !== this.forgetForm.passwordConfirm) {
              this.$message.error('两次输入密码不一致，请重新输入')
              return
            }
            if (this.passwordValid(this.forgetForm.password) === false) {
              return
            }
            if (this.verifyEmail(this.forgetForm.email) === false) {
              return
            }
            if (this.firstEmail !== this.forgetForm.email) {
              this.$message.error('您输入的邮箱与获取验证码的邮箱不一致！')
              return
            }
            const param = {
              password: this.forgetForm.password,
              passwordConfirm: this.forgetForm.passwordConfirm,
              email: this.forgetForm.email,
              fronted_email_code: this.forgetForm.code
            }
            const res = await modifyPassword(param)
            if (res.ResCode === 0) {
              this.$message({
                type: 'success',
                message: '修改密码成功'
              })
              this.forgetDialogTableVisible = false
            } else {
              this.$message({
                type: 'error',
                message: res.ErrMsg
              })
              return
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
    watch: {}
  }
}
</script>

<style lang="less">
@import "../style/mixin";
.login_page {
  background-color: #63647c;
}
.manage_tip {
  position: absolute;
  width: 100%;
  top: -100px;
  left: 0;
  p {
    font-size: 34px;
    color: #fff;
  }
}
.form_contianer {
  .wh(320px, 228px);
  .ctp(320px, 210px);
  padding: 25px;
  border-radius: 5px;
  text-align: center;
  background-color: rgba(240, 243, 244, 0.774);
  .submit_btn {
    width: 100%;
    font-size: 16px;
  }
}
.tip {
  font-size: 12px;
  color: red;
}
.form-fade-enter-active,
.form-fade-leave-active {
  transition: all 1s;
}
.form-fade-enter,
.form-fade-leave-active {
  transform: translate3d(0, -50px, 0);
  opacity: 0;
}
.form {
  min-width: 200px;
  margin-bottom: 10px;
  &:hover {
    box-shadow: 0 0 8px 0 rgba(232, 237, 250, 0.6),
      0 2px 4px 0 rgba(232, 237, 250, 0.5);
    border-radius: 6px;
    transition: all 400ms;
  }
}
.info_form {
  border: 1px solid #dfe1e9;
  padding: 10px 10px 0;
  background-color: #dbe9cb;
}
.dialog {
  background-color: #adcce9;
}
.avatar-uploader .el-upload {
  border: 1px dashed #20a0ff;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}
.avatar-uploader .el-upload:hover {
  border-color: #e70808;
}
.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 120px;
  height: 120px;
  line-height: 120px;
  text-align: center;
}
.avatar {
  width: 120px;
  height: 120px;
  display: block;
}
.cell {
  text-align: center;
}
</style>
