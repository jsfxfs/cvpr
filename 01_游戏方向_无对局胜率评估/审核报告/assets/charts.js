(function () {
  var style = getComputedStyle(document.documentElement);
  var accent = style.getPropertyValue('--accent').trim();
  var accent2 = style.getPropertyValue('--accent2').trim();
  var ink = style.getPropertyValue('--ink').trim();
  var muted = style.getPropertyValue('--muted').trim();
  var rule = style.getPropertyValue('--rule').trim();
  var bg2 = style.getPropertyValue('--bg2').trim();
  var ok = style.getPropertyValue('--ok').trim();
  var warn = style.getPropertyValue('--warn').trim();

  // --- Chart 1: 质疑清单严重度 ---
  var qNames = [
    'Q9 数学细节小错（×5!、WLS/MAP）',
    'Q7 排序停止准则对象不明',
    'Q10 “成熟范式”表述过强',
    'Q8 novelty 叙事缺两个真正先例',
    'Q5 GP 覆盖 10¹⁵ 的声明过强',
    'Q6 专家盲测设计不成立',
    'Q4 KO2001 “同构”术语误用',
    'Q3 校准循环性与“客观参照物”悖论',
    'Q2 成对评估函数与 BT 差式矛盾',
    'Q1 BT 传递性 vs 风格克制不可传递'
  ];
  var qScores = [0.5, 1, 1, 2, 2, 2, 3, 3, 3, 3];
  var qColors = qScores.map(function (v) {
    if (v >= 3) return accent2;
    if (v >= 2) return warn;
    return muted;
  });
  var c1 = echarts.init(document.getElementById('chart-severity'), null, { renderer: 'svg' });
  c1.setOption({
    animation: false,
    grid: { left: 10, right: 60, top: 10, bottom: 24, containLabel: true },
    xAxis: {
      type: 'value', max: 3.4, min: 0,
      axisLabel: { show: false }, splitLine: { lineStyle: { color: rule } },
      axisLine: { lineStyle: { color: rule } }
    },
    yAxis: {
      type: 'category', data: qNames, inverse: false,
      axisLabel: { color: ink, fontSize: 12 },
      axisLine: { lineStyle: { color: rule } }, axisTick: { show: false }
    },
    tooltip: {
      appendToBody: true,
      formatter: function (p) {
        var lvl = p.value >= 3 ? '致命' : (p.value >= 2 ? '高' : (p.value >= 1 ? '中' : '低'));
        return p.name + '<br/>严重度：' + lvl;
      }
    },
    series: [{
      type: 'bar',
      data: qScores.map(function (v, i) { return { value: v, itemStyle: { color: qColors[i] } }; }),
      barWidth: 16,
      label: {
        show: true, position: 'right', color: ink, fontSize: 12, fontWeight: 600,
        formatter: function (p) {
          return p.value >= 3 ? '致命' : (p.value >= 2 ? '高' : (p.value >= 1 ? '中' : '低'));
        }
      }
    }]
  });

  // --- Chart 2: 研究价值五维评估 ---
  var c2 = echarts.init(document.getElementById('chart-value'), null, { renderer: 'svg' });
  c2.setOption({
    animation: false,
    tooltip: { appendToBody: true },
    radar: {
      indicator: [
        { name: '问题真实性', max: 5 },
        { name: '方法新颖性', max: 5 },
        { name: '可检验性', max: 5 },
        { name: '工程可行性', max: 5 },
        { name: '就业可迁移性', max: 5 }
      ],
      radius: '68%',
      axisName: { color: ink, fontSize: 13 },
      splitLine: { lineStyle: { color: rule } },
      splitArea: { areaStyle: { color: [bg2, 'transparent'] } },
      axisLine: { lineStyle: { color: rule } }
    },
    series: [{
      type: 'radar',
      data: [{
        value: [5, 3, 3, 4, 4],
        name: '本课题评分',
        areaStyle: { color: accent + '33' },
        lineStyle: { color: accent, width: 2 },
        itemStyle: { color: accent }
      }]
    }]
  });

  // --- Chart 3: 声明核查结果分布 ---
  var c3 = echarts.init(document.getElementById('chart-verdict'), null, { renderer: 'svg' });
  c3.setOption({
    animation: false,
    tooltip: { appendToBody: true, trigger: 'item' },
    legend: { bottom: 0, textStyle: { color: ink } },
    series: [{
      type: 'pie', radius: ['38%', '66%'], center: ['50%', '44%'],
      label: { color: ink, formatter: '{b}\n{c} 项' },
      labelLine: { lineStyle: { color: muted } },
      data: [
        { value: 9, name: '核实无误', itemStyle: { color: ok } },
        { value: 6, name: '成立但需降调', itemStyle: { color: warn } },
        { value: 4, name: '有误/需重写', itemStyle: { color: accent2 } },
        { value: 2, name: '无法核验', itemStyle: { color: muted } }
      ]
    }]
  });

  window.addEventListener('resize', function () {
    c1.resize(); c2.resize(); c3.resize();
  });
})();
