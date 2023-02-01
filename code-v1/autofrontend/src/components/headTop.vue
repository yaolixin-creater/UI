<template>
  <div class="header_container">
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item v-for="(item, index) in $route.meta.title" :key="index">{{item}}</el-breadcrumb-item>
    </el-breadcrumb>
    <el-dropdown @command="handleCommand" trigger="click">
    <span class="el-dropdown-link">
        {{username}}<i class="el-icon-arrow-down el-icon--right"></i>
      </span>
    
      <el-dropdown-menu slot="dropdown">
        <el-dropdown-item command="home">首页</el-dropdown-item>
        <el-dropdown-item command="signout">退出</el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown>
  </div>
</template>

<script>
import { signout } from "@/api/getData";
import { baseImgPath } from "@/config/env";
import { mapActions, mapState } from "vuex";
import { clearToken } from "@/config/common";
export default {
  data() {
    return {
      baseImgPath
    };
  },
  created() {},
  computed: {
    ...mapState(["adminInfo"]),
    username(){
      return localStorage.getItem('autoUsernameForRemember')
    }
  },
  methods: {
    ...mapActions(["getAdminData"]),
    async handleCommand(command) {
      if (command == "home") {
        this.$router.push("/home");
      } else if (command == "signout") {
        try {
          clearToken();
          if (!localStorage.autoTokenForVerify) {
            this.$message({
              type: "success",
              message: "退出成功"
            });
            this.$router.push("/login");
          }
        } catch (err) {
          this.$message({
            type: "error",
            message: err
          });
        }
      }
    }
  }
};
</script>

<style lang="less">
@import "../style/mixin";
.header_container {
  background-color: cornflowerblue;
  height: 50px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-left: 20px;
  padding-right: 20px
}
.avator {
  .wh(36px, 36px);
  border-radius: 50%;
  margin-right: 37px;
}
.el-dropdown-menu__item {
  text-align: center;
}
.el-dropdown {
    display: inline-block;
    position: relative;
    color: #FFFFFF;
    font-size: 14px;
}
</style>