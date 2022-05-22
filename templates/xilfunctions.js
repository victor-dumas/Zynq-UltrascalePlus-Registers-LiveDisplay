function insertFooter() {
  var fileName = location.pathname.substring(location.pathname.lastIndexOf("/") + 1);
  fileName = fileName.substring(0,fileName.lastIndexOf("."));
  var footerText="<br/><table class=noborder width=100%><tr><td class=noborder width=78%>UG1087 (v1.8) July 30, 2021&nbsp;&nbsp;&#169; Copyright 2015-2021 <a href=https://www.xilinx.com target=_blank>Xilinx Inc.</a> All rights reserved.</td><td class=noborder width=22% align=right><a href=https://www.xilinx.com/about/feedback/document-feedback.html?docType=User_Guides&docId=UG1087&Title=Zynq%20UltraScale%2B%20Devices%20Register%20Reference&releaseVersion=1.8&docPage=" + fileName + " target=_blank><img src={{url_for('static', filename='feedback_icon_true_size_e.png')}} height=23px width=87px border=0></a></td></tr></table>";
  document.getElementById("foot").innerHTML=footerText;
}
window.onload=insertFooter;

function gotoTopic(thisTopic) {
  if (window.top != window.self) {
    window.self.location.href = thisTopic;
  } else {
    window.top.location.href="./ug1087-zynq-ultrascale-registers.html#" + thisTopic;
  }
  return false;
}
