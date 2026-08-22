(function () {
  var style = getComputedStyle(document.documentElement);
  var accent = style.getPropertyValue('--accent').trim();
  var accent2 = style.getPropertyValue('--accent2').trim();
  var ink = style.getPropertyValue('--ink').trim();
  var muted = style.getPropertyValue('--muted').trim();
  var rule = style.getPropertyValue('--rule').trim();
  var bg2 = style.getPropertyValue('--bg2').trim();
  var ok = style.getPropertyValue('--ok').trim();

  var SKILLS = [
    'brain-deepExplore', 'wq-brain-campaign-matrix', 'wq-brain-campaign-toolkit',
    'brain-nextMove-analysis', 'brain-forum-browse', 'wq-brain-ppa-mining',
    'brain-dataset-exploration-general', 'brain-datafield-exploration-general',
    'brain-data-feature-engineering', 'brain-makeSomeGem', 'brain-feature-implementation',
    'brain-enhance-template', 'alpha-expression-verifier',
    'brain-inspectRawTemplate-create-Setting', 'brain-simAlphasinBatch-and-track',
    'wqb-concurrency', 'brain-how-to-pass-AlphaTest', 'wq-brain-alpha-optimization-v1',
    'brain-calculate-alpha-selfcorrQuick', 'brain-explain-alphas', 'brain-alpha-judge',
    'worldquant-submit-alpha', 'wq-brain-superalpha', 'wq-backtest-monitor'
  ];
  var DIMS = ['SKILL.md', '无乱码', 'frontmatter', 'last_verified', '无断链'];
  var selfcorrIdx = SKILLS.indexOf('brain-calculate-alpha-selfcorrQuick');
  var hdata = [];
  SKILLS.forEach(function (_, yi) {
    DIMS.forEach(function (_, xi) {
      var v = (xi === 3 && yi !== selfcorrIdx) ? 0 : 1;
      hdata.push([xi, yi, v]);
    });
  });

  var heat = echarts.init(document.getElementById('chart-heat'), null, { renderer: 'svg' });
  heat.setOption({
    animation: false,
    grid: { top: 30, left: 8, right: 80, bottom: 40, containLabel: true },
    tooltip: {
      appendToBody: true,
      position: 'top',
      formatter: function (p) {
        return SKILLS[p.value[1]] + ' · ' + DIMS[p.value[0]] + '：' + (p.value[2] === 1 ? '通过' : '缺失');
      }
    },
    xAxis: {
      type: 'category', data: DIMS, splitArea: { show: false },
      axisLine: { lineStyle: { color: rule } },
      axisLabel: { color: ink, fontWeight: 600 }
    },
    yAxis: {
      type: 'category', data: SKILLS, splitArea: { show: false },
      axisLine: { show: false }, axisTick: { show: false },
      axisLabel: { color: muted, width: 220, overflow: 'truncate', fontSize: 11 }
    },
    visualMap: {
      min: 0, max: 1, show: false,
      inRange: { color: [accent2, ok] }
    },
    series: [{
      type: 'heatmap', data: hdata,
      label: {
        show: true,
        formatter: function (p) { return p.value[2] === 1 ? '✓' : '✗'; },
        color: '#ffffff', fontWeight: 700
      },
      itemStyle: { borderWidth: 0 },
      emphasis: { itemStyle: { borderColor: ink, borderWidth: 2 } }
    }]
  });
  window.addEventListener('resize', function () { heat.resize(); });

  var sev = echarts.init(document.getElementById('chart-sev'), null, { renderer: 'svg' });
  sev.setOption({
    animation: false,
    color: [accent2, '#e0a000', muted],
    tooltip: { appendToBody: true, formatter: '{b}<br/>{c} 项' },
    legend: { bottom: 0, textStyle: { color: muted } },
    series: [{
      type: 'pie', radius: ['46%', '72%'], center: ['50%', '44%'],
      label: { color: ink, formatter: '{b} {c}' },
      itemStyle: { borderColor: bg2, borderWidth: 2 },
      data: [
        { name: 'P1 阻断', value: 1 },
        { name: 'P2 一致', value: 3 },
        { name: 'O 观察', value: 2 }
      ]
    }]
  });
  window.addEventListener('resize', function () { sev.resize(); });

  var gate = echarts.init(document.getElementById('chart-gate'), null, { renderer: 'svg' });
  gate.setOption({
    animation: false,
    color: [accent],
    tooltip: { appendToBody: true, trigger: 'axis', axisPointer: { type: 'shadow' } },
    grid: { left: 40, right: 20, top: 20, bottom: 40 },
    xAxis: {
      type: 'category',
      data: ['内部严线', '平台硬线', '双线(内部+平台)', '无关(引擎/横切)'],
      axisLine: { lineStyle: { color: rule } }, axisLabel: { color: ink }
    },
    yAxis: {
      type: 'value', name: 'skill 数', minInterval: 1,
      axisLine: { lineStyle: { color: rule } }, axisLabel: { color: muted },
      nameTextStyle: { color: muted }
    },
    series: [{
      type: 'bar', barWidth: 44,
      label: { show: true, position: 'top', color: ink, fontWeight: 700 },
      data: [
        { value: 3, itemStyle: { color: ok } },
        { value: 3, itemStyle: { color: ok } },
        { value: 2, itemStyle: { color: accent } },
        { value: 2, itemStyle: { color: muted } }
      ]
    }]
  });
  window.addEventListener('resize', function () { gate.resize(); });
})();