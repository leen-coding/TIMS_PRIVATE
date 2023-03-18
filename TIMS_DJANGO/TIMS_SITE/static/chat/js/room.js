var ClutchindicatorStatus = document.getElementById("Clutchindicator-status");
var ClutchindicatorText = document.getElementById("Clutchindicator-text");
var StartindicatorStatus = document.getElementById("Startindicator-status");
var StartindicatorText = document.getElementById("Startindicator-text");
var OmniStartindicatorStatus = document.getElementById("Omniindicator-status");
var OmniStartindicatorText = document.getElementById("Omniindicator-text");
var MicrotindicatorStatus = document.getElementById("Microindicator-status");
var MicroindicatorText = document.getElementById("Microindicator-text");

var url = document.URL;
const regex = /\/\/([\d\w\.-]+):(\d+)\//;
const match = url.match(regex);
const ip = match[1];

console.log(ip);
const img1 = document.getElementById('img1');
img1.src = `http://${ip}:8080/cam/1/`;
const img2 = document.getElementById('img2');
img2.src = `http://${ip}:8080/cam/2/`;

const roomName = JSON.parse(document.getElementById('room-name').textContent);
const throttle = (fn, delay) => {
  let lastCall = 0;
  return function (...args) {
    const now = new Date().getTime();
    if (now - lastCall < delay) {
      return;
    }
    lastCall = now;
    return fn(...args);
  };
};

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);

var gchartDom = document.getElementById('gauges');
var gmyChart = echarts.init(gchartDom,'dark');
var goption;
gmyChart.showLoading();
function refreshData(data){
    gmyChart.hideLoading();
  gmyChart.setOption({
  tooltip: {
    formatter: '{a} <br/>{b} : {c}%'
  },
  series: [
    {
      name: 'FORCE',
      type: 'gauge',
      progress: {
        show: true
      },

      detail: {
        valueAnimation: true,
        formatter: '{value}',
          fontSize: 10
      },
      data: [
        {
          value: data,
          name: 'FORCE'
        }
      ]
    }
    ]}
  )}
////////////////////////////
var pchartDom = document.getElementById('ping');
var pmyChart = echarts.init(pchartDom,'dark');
var poption;
pmyChart.showLoading();
function refreshDataPing(data){
    pmyChart.hideLoading();
  pmyChart.setOption({
  tooltip: {
    formatter: '{a} <br/>{b} : {c}%'
  },
  series: [
    {
      name: 'PING',
      type: 'gauge',
      progress: {
        show: true
      },

      detail: {
        valueAnimation: true,
        formatter: '{value}',
          fontSize: 10
      },
      data: [
        {
          value: data,
          name: 'PING'
        }
      ]
    }
    ]}
  )}
const throttledDrawPing = throttle(refreshDataPing, 1000 / 3);
///////////////

const throttledDraw = throttle(refreshData, 1000 / 3);

var chartDom = document.getElementById('main');
var myChart3D = echarts.init(chartDom,'dark');
var option;
var dataQueue = [];
myChart3D.showLoading();
// 初始化图表的配置
var symbolSize = 2.5;
var sizeValue = '57%';
option = {
    grid3D: {
        width: '50%'
    },
    xAxis3D: {
        type: 'value',
        min: 9000,
        max: 17000,
        name: 'X'
    },
    yAxis3D: {
        type: 'value',
        min: -17460,
        max: -8754,
        name: 'Y'
    },
    zAxis3D: {
        type: 'value',
        min: -15696,
        max: -8652,
        name: 'Z'
    },

    grid: [
        { left: '50%', width: '20%', bottom: sizeValue },
        { left: '75%', width: '20%', bottom: sizeValue },
        { left: '50%', width: '20%', top: sizeValue },
        { left: '75%', width: '20%', top: sizeValue }
    ],
    xAxis: [
        {
          type: 'category',
          gridIndex: 0,
          name: 'T', axisTick: {show: false}, axisLine: {show: false},axisLabel:{"show":false} ,

        },
        {
            type: 'category',
            gridIndex: 1,
            name: 'T',axisTick: {show: false},axisLine: {show: false},
            axisLabel:{"show":false} ,
        },
         {
             type: 'category',
            gridIndex: 2,
            name: 'T',axisTick: {show: false},axisLine: {show: false},
            axisLabel:{"show":false} ,
         },
         {
             type: 'category',
            gridIndex: 3,
            name: 'T',axisTick: {show: false},axisLine: {show: false},
            axisLabel:{"show":false} ,
        }
     ],
    yAxis: [
        { boundaryGap: [0, '50%'],type: 'value', gridIndex: 0, name: 'X' },
        {boundaryGap: [0, '50%'], type: 'value', gridIndex: 1, name: 'Y' },
        { boundaryGap: [0, '50%'],type: 'value', gridIndex: 2, name: 'Z' },
        {boundaryGap: [0, '50%'], type: 'value', gridIndex: 3, name: 'R' }
     ],
    progressive : 100,
    progressiveThreshold :100,
    dataset: {
    dimensions: [
    'X',
    'Y',
    'Z','R','T'
    ],
    source: dataQueue
    },
    series: [

        {
    type: 'line3D',

    encode: {
    x: 'X',
    y: 'Y',
    z: 'Z'
     }
    },
        {
  type: 'line',
  symbolSize: symbolSize,
  xAxisIndex: 0,
  yAxisIndex: 0,
  encode: {
    x: 'T',
    y: 'X',
    tooltip: [0, 1, 2, 3, 4]
  }
},
{
  type: 'line',
  symbolSize: symbolSize,
  xAxisIndex: 1,
  yAxisIndex: 1,
  encode: {
    x: 'T',
    y: 'Y',
    tooltip: [0, 1, 2, 3, 4]
  }
},
{
  type: 'line',
  symbolSize: symbolSize,
  xAxisIndex: 2,
  yAxisIndex: 2,
  encode: {
    x: 'T',
    y: 'Z',
    tooltip: [0, 1, 2, 3, 4]
  }
},
                {
  type: 'line',
  symbolSize: symbolSize,
  xAxisIndex: 3,
  yAxisIndex: 3,
  encode: {
    x: 'T',
    y: 'R',
    tooltip: [0, 1, 2, 3, 4]
  }
}
]
};

myChart3D.setOption(option);

function refreshData3D(){
    option.dataset.source = dataQueue;
    myChart3D.hideLoading();
    myChart3D.setOption(option);
}
const throttledDraw3D = throttle(refreshData3D, 1000 / 3);


var last_force = 0;
var seq = 0;
var last_x = 0;
var last_y = 0;
var last_z = 0;
var last_r = 0;
var micro_time = 0;
var omni_time = 0;
var omni_force = 0;
var omniFirst = 1;
var microFirst = 1;
var fistStop = 1;
var lastStage = 0;
chatSocket.onmessage = function(e) {

    const data = JSON.parse(e.data);

    if (data.message.dev === "omni"){
        document.querySelector('#omni_info').innerHTML = (JSON.stringify(data.message) + '\n');
        omni_force = Math.floor(data.message.force*100);
        var foot_y = data.message.foot_y;
        var foot_x = data.message.foot_x;
        var foot_z = data.message.foot_z;
        omni_time = Math.floor(data.message.time/2e6);

        throttledDraw(omni_force);
        if (omniFirst){
            OmniStartindicatorStatus.checked = true;
            OmniStartindicatorText.innerHTML = "OMNI START";
            OmniStartindicatorText.style.color = "#100c2a";
            omniFirst = 0;
        }


        if(foot_x){
            StartindicatorStatus.checked = true;
            StartindicatorText.innerHTML = "SYS ON";
            StartindicatorText.style.color = "#100c2a";
        }
        if(foot_z && fistStop){

            StartindicatorStatus.checked = false;
            StartindicatorText.innerHTML = "SYS STOP";
            StartindicatorText.style.color = "white";

            OmniStartindicatorStatus.checked = false;
            OmniStartindicatorText.innerHTML = "OMNI STOP";
            OmniStartindicatorText.style.color = "white";

            MicrotindicatorStatus.checked = false;
            MicroindicatorText.innerHTML = "MICRO STOP";
            MicroindicatorText.style.color = "white";
            fistStop = 0;
        }
        if(foot_y){
            ClutchindicatorStatus.checked = true;
            ClutchindicatorText.innerHTML = "CLUTCHING OFF";
            ClutchindicatorText.style.color = "#100c2a";
        }
        else {
            ClutchindicatorStatus.checked = false;
            ClutchindicatorText.innerHTML = "CLUTCHING ON";
            ClutchindicatorText.style.color = "white";
        }


    }


    else if (data.message.dev === "micro")
    {
         document.querySelector('#micro_info').innerHTML = (JSON.stringify(data.message) + '\n');
        var new_x =data.message.x
        var new_y = -data.message.y
        var new_z = -data.message.z
        var new_r =data.message.r
        var new_stage = data.message.taskFlag
        if (lastStage !== new_stage){
            if (new_stage === 1){
                showMessage("Line Following Task Start!",2000)

            }
            else if(new_stage === 2){
                showMessage("Line Following Task Finish! Plz Release the FootPedal!",6000)
            }
            else{
                showMessage("Eye Poking Task Start!",2000)
            }
            lastStage = new_stage
        }
        micro_time = Math.floor((data.message.time)/2e6 );

        if (microFirst){

            MicrotindicatorStatus.checked = true;
            MicroindicatorText.innerHTML = "MICRO START";
            MicroindicatorText.style.color = "#100c2a";
            microFirst = 0;
        }

        if(new_x!==last_x || new_y!==last_y ||new_z!==last_z || new_r!==last_r){
            let newData = [new_x,new_y,new_z,new_r,seq]
            last_x = new_x;
            last_y = new_y;
            last_z = new_z;
            last_r = new_r;
            seq = seq + 1;
            dataQueue.push(newData);
              if (dataQueue.length > 5000) {
                dataQueue.shift(); // 移除队列头元素
              }
            throttledDraw3D();
        }


    }

    else{
        document.querySelector('#tactile_info').innerHTML = (JSON.stringify(data.message) + '\n');
    }
    let latency = 0;
    if (micro_time === 0 || omni_time === 0 ||fistStop === 0){
        latency = 0;
    }
    else{
        latency =Math.abs(Math.abs(micro_time - omni_time));
    }

    throttledDrawPing(latency);


};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};




function showMessage(messageText, timeout) {
  var message = document.createElement("div");
  message.innerHTML = messageText;
  message.style.position = "fixed";
  message.style.top = "50%";
  message.style.left = "50%";
  message.style.transform = "translate(-50%, -50%)";
  message.style.backgroundColor = "lightyellow";
  message.style.padding = "20px";
  message.style.border = "1px solid gray";
  message.style.width = "0";
  message.style.textAlign = "center";
  message.style.fontSize = "18px";
  message.style.opacity = "0";
  message.style.transition = "all 0.5s ease-in-out";
  document.body.appendChild(message);

  setTimeout(function() {
    message.style.width = "300px";
    message.style.opacity = "1";
  }, 100);

  setTimeout(function() {
    message.style.display = "none";
  }, timeout);
}


