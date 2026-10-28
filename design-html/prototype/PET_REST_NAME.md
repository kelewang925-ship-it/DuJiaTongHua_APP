# 宠物休息页昵称与长文本修复

范围：m07-p07及其实际加载的共享昵称脚本。完整目标仍为八模块114页、原提示词41项及七类交付物。

真实宠物已改名为奶糖，休息区仍显示“糯米想先睡一会儿”。根因是已有昵称替换遍历漏了h2。原逻辑加入h2；扫描全部11个脚本使用页，带原示例姓名的h2只有此页。保存、库存、精力计算及导航回调保持原字节。

休息标题与说明使用同一纵向容器，给12字昵称留出换行空间。顶部标题及精力说明限制在各自原有区域内，避免长昵称覆盖横幅或超出屏幕；保留完整真实姓名。

运行 `verify_pet_rest_name.py --stage current`，再运行 `verify_pet_rest_checkpoint.py`。需要本机8765预览服务及既有Playwright环境。

- [失败基线](evidence/baseline/pet-rest-name/results.json)：五宽度×中文短名／英文名／12字中文名共15项，全部复现旧标题。
- [中间失败](evidence/current/pet-rest-name/header-overlap/results.json)：18项中13项通过，五种宽度的长昵称均挤到横幅。
- [最终浏览器报告](evidence/current/pet-rest-name/results.json)：15种文本与宽度组合、原三个入口、共享脚本11页加载与标题检查，共29项。
- [源码范围核对](evidence/current/pet-rest-name/checkpoint.json)：精确撤销声明的CSS、结构包装及一个选择器修改后，与保存的源码逐字节相等；custom/pages镜像相等。
- [普通昵称截图](evidence/current/pet-rest-name/390-奶糖.png)／[12字昵称截图](evidence/current/pet-rest-name/390-long.png)已实际查看。Chrome、DPR、语言及时区见报告；390×844仍为临时检查条件。

扩展加载检查首次有两项测试夹具错误：领养前宠物为null，测试直接写name。保留在smoke-null-fixture目录，测试改为尊重未领养状态，产品未为测试修改。rest-only、layout-18目录保留中间报告及实际执行脚本。

这批只证明报告列出的场景。其他宠物页头像、气泡、图标避让和静态试穿／奖励／进度插画问题继续开放。原稿自检仍94/114，人工验收仍0，开发／交互／视觉状态不提升。

工作区另有回忆册V2改动，未包含在本批提交和本批核验范围。既有全量源指纹报告保留，不能用本次检查宣称新回忆册或全部114页重新通过。
