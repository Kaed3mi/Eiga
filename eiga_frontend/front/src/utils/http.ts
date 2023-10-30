import axios from "axios";  // 要导入安装的包，则直接填写包名即可。不需要使用路径
 
// 实例化
const http = axios.create({
    //baseURL: 'http://wthrcdn.etouch.cn/',    // 请求的公共路径,一般填写服务端的默认的api地址，这个地址在具体使用的时候覆盖
    baseURL: 'http://127.0.0.1:8000/vue/',    // 请求的公共路径,一般填写服务端的默认的api地址，这个地址在具体使用的时候覆盖
    timeout: 8000,                           // 最大请求超时时间，请求超过这个时间则报错，有文件上传的站点不要设置这个参数
    //headers: {'X-Custom-Header': 'foobar'}   // 默认的预定义请求头，一般工作中这里填写隐藏了客户端身份的字段
});
 
export default http;