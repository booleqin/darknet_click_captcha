# darknet_click_captcha

基于Darknet框架识别点选验证码。**注：这里只提供方法，不提供具体的模型**

本说明是预测，训练过程分解见：[文字点选验证码识别-darknet](http://booleflow.com/2021/02/27/wen-zi-dian-xuan-yan-zheng-ma-shi-bie-darknet/)

## 概览

对预测服务进行了简单封装，把三个模型填充进去，支持支持基于目标框检测+文字识别的坐标点预测。

服务部署主要包含4部分，分别是

YOLO预测框架部署
配置文件修改
启动方式
参数格式化

## YOLO预测框架部署

在./darknet目录下

预测框架为darknet，其基于C语言编写，比python版本的YOLO预测效率更高，已经进行较高的封装，解压后make编译即可。

解压 该目录下的 master.zip 文件

在CPU上运行时，Makefile文件可以不用修改，直接进行编译

如果在GPU上，还需要修改三个配置参数：

OPENCV=0 修改为 OPENCV=1
GPU=0 修改为 GPU=1
CUDNN=0 修改为 CUDNN=1
编译方法如下：

```shell
cd darknet-master  # 这是解压后的目录
make  # 执行编译操作
```

如果报错 cc1: error: invalid option argument '-Ofast' 可以更新gcc版本，或者再安装一个gcc，在编译的时候指定gcc版本，如下

```shell
make CC=/opt/gcc53/bin/gcc CPP=/opt/gcc53/bin/g++ CXX=/opt/gcc53/bin/g++ LD=/opt/gcc53/bin/g++
```

如果没有报错，那预测框架就算OK了

## 修改配置文件
需要修改的配置文件主要有4个

其中3个是模型预测的meta文件，必须修改（这三个文件修改内容基本一致，没有统一在预测文件中getcwd拼接是为了模型的训练与预测更加灵活）。另一个是服务端口配置，如果端口没有被占用（当前端口8713），可选修改。

必须修改文件1：./detect/img_colour/word.meta

把 xxx 修改为部署的跟目录即可

```shell
classes=1  # 不需修改
train=/xxx/detect/img_colour/train.list
valid=/xxx/detect/img_colour/test.list
names=/xxx/detect/img_colour/word.labels
backup=/xxx/detect/img_colour/backup
top=5  # 不需修改
```

必须修改文件2：./detect/img_white/word.meta

```shell
classes=1
train=/xxx/detect/img_white/train.list
valid=/xxx/detect/img_white/test.list
names=/xxx/detect/img_white/word.labels
backup=/xxx/detect/img_white/backup
top=5
```

必须修改文件3：./classifier/class.meta

```shell
classes=4313
train=/xxx/classifier/train.list
valid=/xxx/classifier/test.list
names=/xxx/classifier/class.labels
backup=/xxx/classifier/backup
top=5
```

可选修改文件4：./conf/service.conf

```shell
# model service conf

[ServicePlat]
plat = test

[test]
host = 0.0.0.0
port = 8713

[online]
host = 0.0.0.0
port = 8713
```

## 启动方式
start 和 stop 命令封装在了 service_run 文件中

```shell
sh service_run start  # 启动
sh service_run stop  # 终止
```

如果启动后在 ./log/flask.log.$date 中出现如下加载模型的日志，则说明启动成功

```shell
Loading weights from /xxx/detect/img_colour/backup/word_final.weights...Done!
layer     filters    size              input                output
    0 conv     32  3 x 3 / 1   256 x 256 x   3   ->   256 x 256 x  32  0.113 BFLOPs
    1 max          2 x 2 / 2   256 x 256 x  32   ->   128 x 128 x  32
    2 conv     64  3 x 3 / 1   128 x 128 x  32   ->   128 x 128 x  64  0.604 BFLOPs
    3 max          2 x 2 / 2   128 x 128 x  64   ->    64 x  64 x  64
    4 conv    128  3 x 3 / 1    64 x  64 x  64   ->    64 x  64 x 128  0.604 BFLOPs
    5 conv     64  1 x 1 / 1    64 x  64 x 128   ->    64 x  64 x  64  0.067 BFLOPs
    6 conv    128  3 x 3 / 1    64 x  64 x  64   ->    64 x  64 x 128  0.604 BFLOPs
    7 max          2 x 2 / 2    64 x  64 x 128   ->    32 x  32 x 128
    8 conv    256  3 x 3 / 1    32 x  32 x 128   ->    32 x  32 x 256  0.604 BFLOPs
    9 conv    128  1 x 1 / 1    32 x  32 x 256   ->    32 x  32 x 128  0.067 BFLOPs
   10 conv    256  3 x 3 / 1    32 x  32 x 128   ->    32 x  32 x 256  0.604 BFLOPs
   11 max          2 x 2 / 2    32 x  32 x 256   ->    16 x  16 x 256
   12 conv    512  3 x 3 / 1    16 x  16 x 256   ->    16 x  16 x 512  0.604 BFLOPs
   13 conv    256  1 x 1 / 1    16 x  16 x 512   ->    16 x  16 x 256  0.067 BFLOPs
   14 conv    512  3 x 3 / 1    16 x  16 x 256   ->    16 x  16 x 512  0.604 BFLOPs
   15 conv    256  1 x 1 / 1    16 x  16 x 512   ->    16 x  16 x 256  0.067 BFLOPs
   16 conv    512  3 x 3 / 1    16 x  16 x 256   ->    16 x  16 x 512  0.604 BFLOPs
   17 max          2 x 2 / 2    16 x  16 x 512   ->     8 x   8 x 512
   18 conv   1024  3 x 3 / 1     8 x   8 x 512   ->     8 x   8 x1024  0.604 BFLOPs
   19 conv    512  1 x 1 / 1     8 x   8 x1024   ->     8 x   8 x 512  0.067 BFLOPs
   20 conv   1024  3 x 3 / 1     8 x   8 x 512   ->     8 x   8 x1024  0.604 BFLOPs
   21 conv    512  1 x 1 / 1     8 x   8 x1024   ->     8 x   8 x 512  0.067 BFLOPs
   22 conv   1024  3 x 3 / 1     8 x   8 x 512   ->     8 x   8 x1024  0.604 BFLOPs
   23 conv   2236  1 x 1 / 1     8 x   8 x1024   ->     8 x   8 x2236  0.293 BFLOPs
   24 avg                        8 x   8 x2236   ->  2236
   25 softmax                                        2236
```
注：请求时的日志在 ./log/output.log 中，日志配置每 1GB 自动切割一次，保留10个文件，更长时间的日志会自动删除。

## 参数格式化
### 请求地址
host为部署服务的目标机器

http://host:8713/captcha/distinguish 

### 入参
其中的图片文件地址需要在部署服务的机器上，否则会找不到文件

```shell
{
    "model":"classifier",  # 现在只支持 classifier，表示基于文字分类；后续可能会增加 resemblance，基于孪生网络相似性
    "basefile":"/xxx/click_captcha/test_img/white/0a33dacbd4_2.jpg",  # 白低图片文件所在地址
    "objfile":"/xxx/click_captcha/test_img/colour/0a33dacbd4_1.jpg"  # 彩低图片文件地址
}
```

### 出参
返回结果

```shell
{
    "code":0,  # 0表示返回正常。如果为1时，表示返回错误，后面的ret会给出错误的原因，./log/output.log 中会给出详细错误
    "ret":[
        [
            1,  # 点击顺序（1表示第一个点击）
            [
                123.05937957763672,  # 表示需要点击的位置的 x 坐标 （该坐标是图片上的像素坐标，实际模拟点击时需要换算成屏幕上的像素坐标，下同）
                104.45993041992188,  # 表示需要点击的位置的 y 坐标
                67.01766967773438,  # 表示目标框的宽度
                57.632049560546875  # 表示目标框的高度
            ]
        ],
        [
            2,  # 点击顺序（2表示第二个点击）
            [
                36.272579193115234,
                78.7174072265625,
                59.66224670410156,
                52.96824645996094
            ]
        ],
        [
            3,
            [
                209.04656982421875,
                77.37615966796875,
                60.23399353027344,
                63.186256408691406
            ]
        ]
    ]
}
```
