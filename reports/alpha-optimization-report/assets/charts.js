(function() {
  var style = getComputedStyle(document.documentElement);
  var accent = '#3b82f6';
  var accent2 = '#f59e0b';
  var ink = '#e2e8f0';
  var muted = '#94a3b8';
  var green = '#22c55e';
  var red = '#ef4444';
  var yellow = '#eab308';
  var bg2 = '#131c31';
  var rule = '#1e2d4a';

  var commonGrid = {
    left: '8%',
    right: '5%',
    top: '12%',
    bottom: '15%'
  };

  var commonAxis = {
    axisLine: { lineStyle: { color: rule } },
    axisLabel: { color: muted, fontSize: 11 },
    splitLine: { lineStyle: { color: rule, type: 'dashed' } }
  };

  // Chart 1: ProdCorr 优化演进路径
  var chart1 = echarts.init(document.getElementById('chart-prodcorr-trend'));
  chart1.setOption({
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      backgroundColor: bg2,
      borderColor: rule,
      textStyle: { color: ink, fontSize: 12 }
    },
    grid: commonGrid,
    xAxis: {
      type: 'category',
      data: ['b92\n原始\n150d', 'b95\n360d', 'b97\n1080d', 'b98-99\nIV均值/Greeks', 'b100\ntheta差分', 'b102\nSTAT中性化', 'b104\n1:1复合', 'b105\n2:1 theta60', 'b107\nPower10'],
      ...commonAxis,
      axisLabel: { color: muted, fontSize: 10, interval: 0, rotate: 15 }
    },
    yAxis: {
      type: 'value',
      name: 'ProdCorr',
      min: 0.65,
      max: 0.80,
      ...commonAxis,
      nameTextStyle: { color: muted, fontSize: 11 }
    },
    series: [{
      name: 'ProdCorr',
      type: 'line',
      data: [0.7755, 0.7529, 0.7621, null, null, null, 0.7387, 0.724, 0.7295],
      lineStyle: { color: accent, width: 3 },
      itemStyle: { color: accent },
      symbolSize: 10,
      connectNulls: false,
      markLine: {
        silent: true,
        symbol: 'none',
        lineStyle: { color: red, type: 'dashed', width: 2 },
        data: [{ yAxis: 0.7, name: '阈值 0.7', label: { formatter: '阈值 0.7', color: red, fontSize: 11 } }]
      },
      markPoint: {
        symbol: 'pin',
        symbolSize: 50,
        data: [
          { coord: ['b105\n2:1 theta60', 0.724], itemStyle: { color: green }, label: { color: '#fff', fontSize: 10 } }
        ]
      }
    }, {
      name: 'Theta 差分 (SLOW_AND_FAST)',
      type: 'line',
      data: [null, null, null, null, null, null, null, null, null],
      lineStyle: { color: yellow, width: 2, type: 'dashed' }
    }, {
      name: '复合信号',
      type: 'line',
      data: [null, null, null, null, null, null, 0.7387, 0.724, 0.7295],
      lineStyle: { color: green, width: 3 },
      itemStyle: { color: green },
      symbolSize: 10
    }]
  });

  // Chart 2: 信号类型 ProdCorr 对比
  var chart2 = echarts.init(document.getElementById('chart-signal-comparison'));
  chart2.setOption({
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      backgroundColor: bg2,
      borderColor: rule,
      textStyle: { color: ink, fontSize: 12 }
    },
    grid: { ...commonGrid, bottom: '25%' },
    xAxis: {
      type: 'category',
      data: ['IV skew\n(360d)', 'IV skew\n(180d)', 'IV skew\n(1080d)', '1:1 复合', '2:1 复合\n(theta60)', '2:1 复合\n(theta182)', '3:1 复合'],
      ...commonAxis,
      axisLabel: { color: muted, fontSize: 10, interval: 0, rotate: 20 }
    },
    yAxis: {
      type: 'value',
      name: 'ProdCorr',
      min: 0.65,
      max: 0.80,
      ...commonAxis,
      nameTextStyle: { color: muted, fontSize: 11 }
    },
    series: [{
      name: 'ProdCorr',
      type: 'bar',
      data: [
        { value: 0.7529, itemStyle: { color: red } },
        { value: 0.7825, itemStyle: { color: red } },
        { value: 0.7621, itemStyle: { color: red } },
        { value: 0.7387, itemStyle: { color: yellow } },
        { value: 0.724, itemStyle: { color: green } },
        { value: 0.7442, itemStyle: { color: yellow } },
        { value: 0.7483, itemStyle: { color: yellow } }
      ],
      barWidth: '55%',
      label: {
        show: true,
        position: 'top',
        color: ink,
        fontSize: 11,
        formatter: '{c}'
      },
      markLine: {
        silent: true,
        symbol: 'none',
        lineStyle: { color: red, type: 'dashed', width: 2 },
        data: [{ yAxis: 0.7 }]
      }
    }]
  });

  // Chart 3: 权重比例 vs ProdCorr
  var chart3 = echarts.init(document.getElementById('chart-weight-ratio'));
  chart3.setOption({
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      backgroundColor: bg2,
      borderColor: rule,
      textStyle: { color: ink, fontSize: 12 }
    },
    legend: {
      data: ['ProdCorr', 'Sharpe'],
      top: 5,
      textStyle: { color: muted, fontSize: 11 }
    },
    grid: commonGrid,
    xAxis: {
      type: 'category',
      data: ['纯 IV\n(0:1)', '1:1\n(theta182)', '1:1\n(theta60)', '2:1\n(theta60)', '2:1\n(theta182)', '3:1\n(theta60)'],
      ...commonAxis,
      axisLabel: { color: muted, fontSize: 10, interval: 0 }
    },
    yAxis: [
      {
        type: 'value',
        name: 'ProdCorr',
        min: 0.65,
        max: 0.80,
        ...commonAxis,
        nameTextStyle: { color: muted, fontSize: 11 }
      },
      {
        type: 'value',
        name: 'Sharpe',
        min: 1.5,
        max: 2.3,
        axisLine: { lineStyle: { color: rule } },
        axisLabel: { color: muted, fontSize: 11 },
        splitLine: { show: false }
      }
    ],
    series: [{
      name: 'ProdCorr',
      type: 'bar',
      data: [0.7529, 0.7387, 0.7444, 0.724, 0.7442, 0.7483],
      barWidth: '40%',
      itemStyle: {
        color: function(params) {
          return params.dataIndex === 3 ? green : (params.dataIndex === 1 || params.dataIndex === 2 ? yellow : red);
        }
      },
      label: { show: true, position: 'top', color: ink, fontSize: 10 },
      markLine: {
        silent: true,
        symbol: 'none',
        lineStyle: { color: red, type: 'dashed', width: 2 },
        data: [{ yAxis: 0.7 }]
      }
    }, {
      name: 'Sharpe',
      type: 'line',
      yAxisIndex: 1,
      data: [2.03, 1.99, 2.07, 2.03, 1.90, 1.98],
      lineStyle: { color: accent2, width: 2 },
      itemStyle: { color: accent2 },
      symbolSize: 8,
      label: { show: true, position: 'top', color: accent2, fontSize: 10 }
    }]
  });

  // Chart 4: IV 期限 vs ProdCorr (U型曲线)
  var chart4 = echarts.init(document.getElementById('chart-iv-tenor'));
  chart4.setOption({
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      backgroundColor: bg2,
      borderColor: rule,
      textStyle: { color: ink, fontSize: 12 },
      formatter: function(params) {
        var p = params[0];
        return p.name + '<br/>ProdCorr: ' + p.value;
      }
    },
    grid: commonGrid,
    xAxis: {
      type: 'category',
      data: ['20d', '150d', '180d', '270d', '360d', '720d', '1080d'],
      ...commonAxis,
      axisLabel: { color: muted, fontSize: 11 }
    },
    yAxis: {
      type: 'value',
      name: 'ProdCorr',
      min: 0.70,
      max: 0.80,
      ...commonAxis,
      nameTextStyle: { color: muted, fontSize: 11 }
    },
    series: [{
      name: 'ProdCorr',
      type: 'line',
      data: [0.7896, 0.7755, 0.7825, 0.7718, 0.7529, 0.7632, 0.7621],
      lineStyle: { color: accent, width: 3 },
      itemStyle: {
        color: function(params) {
          return params.dataIndex === 4 ? green : accent;
        }
      },
      symbolSize: 12,
      label: {
        show: true,
        position: 'top',
        color: ink,
        fontSize: 10,
        formatter: '{c}'
      },
      markLine: {
        silent: true,
        symbol: 'none',
        lineStyle: { color: red, type: 'dashed', width: 2 },
        data: [{ yAxis: 0.7 }]
      },
      markPoint: {
        symbol: 'pin',
        symbolSize: 45,
        data: [
          { coord: ['360d', 0.7529], itemStyle: { color: green }, label: { color: '#fff', fontSize: 9, formatter: '最低' } }
        ]
      },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: 'rgba(59,130,246,0.2)' },
            { offset: 1, color: 'rgba(59,130,246,0)' }
          ]
        }
      }
    }]
  });

  // Chart 5: Sharpe vs ProdCorr 散点图
  var chart5 = echarts.init(document.getElementById('chart-scatter'));
  chart5.setOption({
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'item',
      backgroundColor: bg2,
      borderColor: rule,
      textStyle: { color: ink, fontSize: 12 },
      formatter: function(params) {
        return params.data.name + '<br/>Sharpe: ' + params.data[0] + '<br/>ProdCorr: ' + params.data[1] + '<br/>' + params.data.desc;
      }
    },
    grid: { ...commonGrid, top: '15%' },
    xAxis: {
      type: 'value',
      name: 'Sharpe',
      min: 1.4,
      max: 2.3,
      ...commonAxis,
      nameTextStyle: { color: muted, fontSize: 11 }
    },
    yAxis: {
      type: 'value',
      name: 'ProdCorr',
      min: 0.70,
      max: 0.85,
      ...commonAxis,
      nameTextStyle: { color: muted, fontSize: 11 }
    },
    series: [{
      name: 'Alpha',
      type: 'scatter',
      symbolSize: function(data) {
        return data.size || 14;
      },
      data: [
        { name: 'A17oXw3g', value: [2.03, 0.724], desc: '2x theta60 + IV360', size: 22, itemStyle: { color: green } },
        { name: 'QP9wR6WG', value: [2.03, 0.724], desc: '2x theta60 + IV1080', size: 20, itemStyle: { color: green } },
        { name: 'xAdJ75ln', value: [2.05, 0.7242], desc: '2x theta60 + IV720', size: 18, itemStyle: { color: green } },
        { name: 'pwK9b67X', value: [2.00, 0.7325], desc: '1:1 IV720 + theta182', size: 16, itemStyle: { color: yellow } },
        { name: 'j2rqK83Z', value: [1.99, 0.7387], desc: '1:1 IV360 + theta182', size: 16, itemStyle: { color: yellow } },
        { name: 'mLVE1LjE', value: [2.03, 0.7529], desc: '纯 IV360 skew', size: 15, itemStyle: { color: accent } },
        { name: '9q7Nmqjr', value: [2.20, 0.7825], desc: '纯 IV180 skew', size: 15, itemStyle: { color: red } },
        { name: 'QP98oPgr', value: [1.58, 0.8111], desc: 'analyst7 convex5', size: 14, itemStyle: { color: red } },
        { name: 'bldezvOr', value: [2.00, 0.7972], desc: 'other566 l2r20_label', size: 14, itemStyle: { color: red } }
      ],
      label: {
        show: true,
        position: 'right',
        color: ink,
        fontSize: 9,
        formatter: function(params) {
          return params.data.name;
        }
      },
      markLine: {
        silent: true,
        symbol: 'none',
        lineStyle: { color: red, type: 'dashed', width: 2 },
        data: [{ yAxis: 0.7, label: { formatter: '阈值', color: red, fontSize: 10 } }]
      },
      markArea: {
        silent: true,
        itemStyle: { color: 'rgba(34,197,94,0.08)' },
        data: [[
          { xAxis: 2.0, yAxis: 0.70 },
          { xAxis: 2.3, yAxis: 0.72 }
        ]]
      }
    }]
  });

  // Responsive
  window.addEventListener('resize', function() {
    chart1.resize();
    chart2.resize();
    chart3.resize();
    chart4.resize();
    chart5.resize();
  });
})();
