<template>
    <div style="margin-top:10px;">
        <Row style="color:black;text-align:center;display:inline">
            <h1> Welcome to student grade managing system! </h1>
        </Row>
    </div>
    <div style="margin-top:20px;">
        <Row>
            <Col span="8" offset="8">
                <Row style="margin-top:10px;">
                    <Col span="4">
                        <h3>ID</h3>
                    </Col>
                    <Col span="20">
                        <Input v-model='name'/>
                    </Col>
                </Row>
                <Row style="margin-top:10px;">
                    <Col span="4">
                        <h3>Password</h3>
                    </Col>
                    <Col span="20">
                        <Input type="password" v-model='password' />
                    </Col>
                </Row>
                <Row style="margin-top:10px;">
                    <Col offset="4" span="20">
                        <Button type="success" long @click='login'> Log In </Button>
                    </Col>
                </Row>
            </Col>
        </Row>
    </div>
</template>

<script>
export default{
    data(){
        return{
            name: '',
            password: '',
        }

    },
    methods:{
        login(){
            if (this.name == '') {
                this.$Message.info('Please Input Your User ID.');
                return;
            }
            if (this.password == '') {
                this.$Message.info('Please Input Your Password.');
                return;
            }
            const param = {name : this.name, password : this.password}
            console.log(param)
            this.$axios({
                withCredentials: true, // 说明：这个地方涉及到了Cookie
                method: "POST",         // 请求方式
                url: import.meta.env.VITE_API_BASE_HOST + "/login", // 本地的主机网址
                data: JSON.stringify(param),  // 说明：这个地方需要js的字符串，因此，需要先将对象转换成字符串
                headers:{
                    'Content-Type': "application/json"
                },
            }).then((res)=>{        // 下面这一堆是处理网断的情况下可能发生的异常
                console.log(res) // 说明：这个地方的res是从后端返回的响应
                if (res.status != 200) {
                    this.$Message.error("Interface Exception (" + res.status + ")")
                    return
                }
                if (res.data.code != 0) {
                    this.$Message.error("登陆失败（ " + res.data.message + ")")
                    return
                }

                this.$Message.success("Log In Successfully!")
                this.$router.push("/students") // 说明：这里学生登录成功之后应该跳转到‘/students’的界面

            }).catch((err)=>{
                this.$Message.error('Network Exception (' + err + ')')
            })
        },
    },
}
</script>
