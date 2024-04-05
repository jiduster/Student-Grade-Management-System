<template>
    <div>
        <Row>
            <Col span="16" offset="4">
                <Row>
                    <Col span="6" style="text-align: left;">
                        <a href="javascript:void(0)" @click="this.$router.push('/teachers')">Teacher Account Management</a>
                    </Col>
                    <Col span="14" style="text-align: right;">
                        <a href="javascript:void(0)" @click="logout">Log Out</a>
                    </Col>
                </Row>
                <Row style="text-align: center; display: inline; margin-top: 10px">
                    <h1>Student Grade Management</h1>
                </Row>
                <Row>
                    <Col offset="10">
                        <Button type="primary" @click="get_student"> Inquire List </Button>
                    </Col>
                    <Col offset="1">
                        <Button type="success" @click="show_add"> Add </Button>
                    </Col>
                </Row>
                <Row style="margin-top: 10px">
                    <Col span="24">
                        <Table :columns="columns" :data="data">
                            <template #action="{row, index}">
                                <Button type="info" size="small" @click="show_modify(row)">Modify</Button>
                                <Button type="error" size="small" style="margin-left: 5px" @click="del_confirm(row)">Delete</Button>
                            </template>
                        </Table>
                    </Col>
                </Row>
            </Col>
        </Row>
    </div>
    <div>
        <Modal
            v-model="add.modal"
            title="Common Modal dialog box title"
            :loading = "add.loading"
            @on-ok="add_ok"
            @on-cancel="add_cancel">
            <p>
                <Row>
                    <Col span="6"> Name </Col>
                    <Col span="18"> <Input  v-model="add.param.name" size="small" style="width: 80%" /> </Col>
                </Row>
                <Row style="margin-top: 10px">
                    <Col span="6"> Chinese </Col>
                    <Col span="18"> <Input  v-model="add.param.chinese" size="small" style="width: 80%" /> </Col>
                </Row>
                <Row style="margin-top: 10px">
                    <Col span="6"> English </Col>
                    <Col span="18"> <Input  v-model="add.param.english" size="small" style="width: 80%" /> </Col>
                </Row>
                <Row style="margin-top: 10px">
                    <Col span="6"> Math </Col>
                    <Col span="18"> <Input  v-model="add.param.math" size="small" style="width: 80%" /> </Col>
                </Row>
            </p>
        </Modal>

        <Modal
            v-model="modify.modal"
            title="Common Modal dialog box title"
            :loading = "modify.loading"
            @on-ok="modify_ok"
            @on-cancel="modify_cancel">
            <p>
                <Row>
                    <Col span="6"> ID </Col>
                    <Col span="18"> <Input  v-model="modify.param.id" disabled size="small" style="width: 80%" /> </Col>
                </Row>
                <Row style="margin-top: 10px">
                    <Col span="6"> Name </Col>
                    <Col span="18"> <Input  v-model="modify.param.name" size="small" style="width: 80%" /> </Col>
                </Row>
                <Row style="margin-top: 10px">
                    <Col span="6"> Chinese </Col>
                    <Col span="18"> <Input  v-model="modify.param.chinese" size="small" style="width: 80%" /> </Col>
                </Row>
                <Row style="margin-top: 10px">
                    <Col span="6"> English </Col>
                    <Col span="18"> <Input  v-model="modify.param.english" size="small" style="width: 80%" /> </Col>
                </Row>
                <Row style="margin-top: 10px">
                    <Col span="6"> Math </Col>
                    <Col span="18"> <Input  v-model="modify.param.math" size="small" style="width: 80%" /> </Col>
                </Row>
            </p>
        </Modal>
    </div>
</template>
<script>
import {Button, Col, Input} from "view-ui-plus";

export default{
    components: {Input, Button, Col},
    data(){
        return{
            modify:{
                modal: false,
                param: {
                    id: '',
                    name: '',
                    english:'',
                    math:'',
                    chinese:'',
                },
                loading: true
            },

            add:{
                modal: false,
                param: {
                    name: '',
                    english:'',
                    math:'',
                    chinese:'',
                },
                loading: true
            },
            // 说明：在这里声明的数据对应的是表单table里面的数据, 用一个json对象的数组表征
            columns:[
                {
                    // 说明：title是对应前端表单的标头字段， key对应的则是后端返回上来的对象里面的字段，如{‘name’：Tom，‘id’：100}
                    //      而align则是说对齐的方式
                    title: 'Student ID',
                    key: 'id',
                    align: 'center',
                },
                {
                  title: 'Name',
                  key: 'name',
                  align: 'center',
                },
                {
                    title: 'Chinese',
                    key: 'chinese',
                    align: 'center',
                },
                {
                    title: 'English',
                    key: 'english',
                    align: 'center',
                },
                {
                    title: 'Math',
                    key: 'math',
                    align: 'center',
                },
                {
                    // 说明：这个地方和表格的其他地方有点不同，因为操作的内容并不是来自后端的数据，而是两个按钮
                    title: 'Operation',
                    slot:'action', // 说明：action需要在table中用template加以处理才能正常显示，因为“ {row，index} ”使得它能遍历索引，在每行都出现
                    minWidth:120,
                },
            ],
            data: [],
        }
    },
    mounted(){
        // 说明：这个是进场自动展示数据
        this.get_student()
    },
    methods: {
        get_student(){
            this.data = [];

            // 向后端发送数据请求
            this.$axios({
                withCredentials: true, // 说明：这个地方涉及到了Cookie
                method: "GET",         // 请求方式
                url: import.meta.env.VITE_API_BASE_HOST + "/student_list", // 本地的学生信息
            }).then((res)=>{        // 下面这一堆是处理网断的情况下可能发生的异常
                console.log(res) // 说明：这个地方的res是从后端返回的响应
                if (res.status != 200) {
                    this.$Message.error("Interface Exception (" + res.status + ")")
                    return
                }
                if (res.data.code == 9999) {
                    this.$Message.error(res.data.message);
                    this.$router.push("/login");
                    return;
                }
                // 说明：如果说返回值的code属性不是0，那么就不是一个正常状态，此时无需额外的赋值操作
                if (res.data.code != 0) {
                    this.$Message.error("Operation Exception (" + res.data.message + ")")
                    return
                }
                this.data = res.data.data   // 这一步直接把返回的数据赋值给了前端的空数组data
            }).catch((err)=>{
                this.$Message.error('Network Exception (' + err + ')')
            })
        },

        add_ok(){
            // 说明：不管怎么说，如果对指定学号的信息进行修改，我们的name都不应该是空的
            if (this.add.param.name == '') {
                this.$Message.error("Name cannot be empty")
                this.add.loading = false
                this.$nextTick(()=>{
                    this.add.loading = true
                })
                return
            }
            let param = {name:this.add.param.name, english:'', chinese:'', math:''}
            if (this.add.param.english != '') {
                param.english = this.add.param.english
            }
            if (this.add.param.math != '') {
                param.math = this.add.param.math
            }
            if (this.add.param.chinese != '') {
                param.chinese = this.add.param.chinese
            }
            // console.log(param)

            // 向后端发送数据请求
            this.$axios({
                withCredentials: true, // 说明：这个地方涉及到了Cookie
                method: "POST",         // 请求方式
                data: JSON.stringify(param),
                url: import.meta.env.VITE_API_BASE_HOST + "/student_add", // 本地的学生信息
                headers:{
                    'Content-Type': "application/json"
                },
            }).then((res)=>{        // 下面这一堆是处理网断的情况下可能发生的异常
                console.log(res) // 说明：这个地方的res是从后端返回的响应
                if (res.status != 200) {
                    this.$Message.error("Interface Exception (" + res.status + ")")
                    return
                }
                if (res.data.code == 9999) {
                    this.$Message.error(res.data.message);
                    this.$router.push("/login");
                    return;
                }
                // 说明：如果说返回值的code属性不是0，那么就不是一个正常状态，此时无需额外的赋值操作
                if (res.data.code != 0) {
                    this.$Message.error("Operation Exception (" + res.data.message + ")")
                    return
                }
                this.add.modal = false;
                this.add_reset() // 操作完成之后直接清空输入框
                this.$Message.success("Student has been added successfully!")
                this.add.loading = false
                this.$nextTick(()=>{
                    this.add.loading = true
                })
                this.get_student()
            }).catch((err)=>{
                this.$Message.error('Network Exception (' + err + ')')
            })

        },

        add_reset(){
            this.add.param.name = ''
            this.add.param.english = ''
            this.add.param.chinese = ''
            this.add.param.math = ''
            this.add.modal = false;
        },

        add_cancel(){
            this.add_reset()
        },
        show_add(){
            this.add.modal = true
        },
        del_confirm(row){
            // console.log(row)  这个地方的row实际上是接收了当前一行的数据
            const self = this
            this.$Modal.confirm({
                title: 'Delete Confirmation',
                content: "Do you really want to delete " + row["name"] + "?",
                onOk(){
                    self.del_submit(row.id)
                },
                onCancel(){
                    return
                }
            })
        },
        del_submit(id){
            // console.log(id)
            const param = {id: id, }
            this.$axios({
                withCredentials: true, // 说明：这个地方涉及到了Cookie
                method: "POST",         // 请求方式
                data: JSON.stringify(param),
                url: import.meta.env.VITE_API_BASE_HOST + "/student_del", // 本地的学生信息
                headers:{
                    'Content-Type': "application/json"
                },
            }).then((res)=>{        // 下面这一堆是处理网断的情况下可能发生的异常
                console.log(res) // 说明：这个地方的res是从后端返回的响应
                if (res.status != 200) {
                    this.$Message.error("Interface Exception (" + res.status + ")")
                    return
                }
                if (res.data.code == 9999) {
                    this.$Message.error(res.data.message);
                    this.$router.push("/login");
                    return;
                }
                // 说明：如果说返回值的code属性不是0，那么就不是一个正常状态，此时无需额外的赋值操作
                if (res.data.code != 0) {
                    this.$Message.error("Operation Exception (" + res.data.message + ")")
                    return
                }

                this.$Message.success("Student has been deleted successfully!")

                this.get_student()
            }).catch((err)=>{
                this.$Message.error('Network Exception (' + err + ')')
            })
        },

        modify_ok(){
            if (this.modify.param.name == '') {
                this.$Message.error("Name cannot be empty")
                this.modify.loading = false
                this.$nextTick(()=>{
                    this.modify.loading = true
                })
                return
            }
            let param = {
                id: this.modify.param.id,
                name:this.modify.param.name,
                english:this.modify.param.english,
                chinese:this.modify.param.chinese,
                math:this.modify.param.math
            }

            this.$axios({
                withCredentials: true, // 说明：这个地方涉及到了Cookie
                method: "POST",         // 请求方式
                data: JSON.stringify(param),
                url: import.meta.env.VITE_API_BASE_HOST + "/student_modify", // 本地的学生信息
                headers:{
                    'Content-Type': "application/json"
                },
            }).then((res)=>{        // 下面这一堆是处理网断的情况下可能发生的异常
                console.log(res) // 说明：这个地方的res是从后端返回的响应
                if (res.status != 200) {
                    this.$Message.error("Interface Exception (" + res.status + ")")
                    return
                }
                if (res.data.code == 9999) {
                    this.$Message.error(res.data.message);
                    this.$router.push("/login");
                    return;
                }
                // 说明：如果说返回值的code属性不是0，那么就不是一个正常状态，此时无需额外的赋值操作
                if (res.data.code != 0) {
                    this.$Message.error("Operation Exception (" + res.data.message + ")")
                    return
                }
                this.modify.modal = false;
                this.modify_reset() // 操作完成之后直接清空输入框
                this.$Message.success("Student has been modified successfully!")
                this.modify.loading = false
                this.$nextTick(()=>{
                    this.modify.loading = true
                })
                this.get_student()
            }).catch((err)=>{
                this.$Message.error('Network Exception (' + err + ')')
            })
        },

        modify_reset(){
            this.modify.param.id = '';
            this.modify.param.name = '';
            this.modify.param.math = '';
            this.modify.param.chinese = '';
            this.modify.param.english = '';
        },

        modify_cancel(){
            this.modify_reset()
            this.modify.modal = false;
        },

        show_modify(row){
            this.modify_reset()

            this.modify.modal = true

            this.modify.param.id = row.id;
            // 说明：这个地方是自动进行填充
            this.modify.param.name = row.name;
            this.modify.param.math = row.math;
            this.modify.param.chinese = row.chinese;
            this.modify.param.english = row.english;
        },

        logout(){
            this.$axios({
                withCredentials: true, // 说明：这个地方涉及到了Cookie
                method: "POST",         // 请求方式
                data: JSON.stringify({}),
                url: import.meta.env.VITE_API_BASE_HOST + "/logout",
                headers:{
                    'Content-Type': "application/json"
                },
            }).then((res)=>{        // 下面这一堆是处理网断的情况下可能发生的异常
                console.log(res) // 说明：这个地方的res是从后端返回的响应
                if (res.status != 200) {
                    this.$Message.error("Interface Exception (" + res.status + ")")
                    return
                }
                if (res.data.code == 9999) {
                    this.$Message.error(res.data.message);
                    this.$router.push("/login");
                    return;
                }
                // 说明：如果说返回值的code属性不是0，那么就不是一个正常状态，此时无需额外的赋值操作
                if (res.data.code != 0) {
                    this.$Message.error("Operation Exception (" + res.data.message + ")")
                    return
                }
                this.$Message.success("Log Out Successfully!")
                this.$router.push("/")
            }).catch((err)=>{
                this.$Message.error('Network Exception (' + err + ')')
            })
        }
    },
}
</script>