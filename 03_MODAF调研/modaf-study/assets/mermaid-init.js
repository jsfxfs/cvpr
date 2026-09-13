(function () {
  if (typeof mermaid === 'undefined') return;

  mermaid.initialize({
    startOnLoad: false,
    theme: 'base',
    securityLevel: 'loose',
    fontFamily: "'Work Sans', 'PingFang SC', 'Microsoft YaHei', sans-serif",
    themeVariables: {
      background: '#f5f6f8',
      primaryColor: '#eaeef3',
      primaryTextColor: '#1d2733',
      primaryBorderColor: '#1f4e79',
      lineColor: '#5a6a7d',
      secondaryColor: '#eaeef3',
      secondaryTextColor: '#1d2733',
      secondaryBorderColor: '#9a4632',
      tertiaryColor: '#f5f6f8',
      tertiaryTextColor: '#1d2733',
      tertiaryBorderColor: '#d7dde5',
      noteBkgColor: '#eaeef3',
      noteTextColor: '#1d2733',
      noteBorderColor: '#d7dde5',
      clusterBkg: '#eaeef3',
      clusterBorder: '#d7dde5',
      edgeLabelBackground: '#f5f6f8',
      actorBkg: '#eaeef3',
      actorBorder: '#1f4e79',
      actorTextColor: '#1d2733',
      signalColor: '#1d2733',
      signalTextColor: '#1d2733',
      labelBoxBkgColor: '#eaeef3',
      labelBoxBorderColor: '#1f4e79',
      labelTextColor: '#1d2733',
      loopTextColor: '#1d2733',
      fontSize: '14px'
    },
    timeline: {
      disableMulticolor: true
    },
    flowchart: {
      curve: 'basis',
      nodeSpacing: 40,
      rankSpacing: 48,
      padding: 12
    }
  });

  mermaid.run({ querySelector: '.mermaid' });
})();
