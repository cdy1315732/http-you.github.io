# Publish Flow

## 标准顺序
1. 用户给题材方向
2. 联网研究热门内容
3. 整理研究笔记
4. 生成标题和正文
5. 生成封面图和内容图
6. 检查小红书登录态
7. 上传并发布
8. 校验发布结果

## 登录和成功判断
- 创作中心正常打开才算可发布
- 如果跳到 `login?redirectReason=401`，说明登录态失效
- 如果出现二维码轮询接口，说明还需要扫码
- 只有同时满足下面两点，才算发布成功：
  - URL 含 `/publish/success`
  - `POST https://edith.xiaohongshu.com/web_api/sns/v2/note` 返回 `200`

## 浏览器 profile
- `xhs`

## 素材处理
- 发布时上传 PNG，不上传 SVG
- 上传前先把素材复制到 `/tmp/openclaw/uploads/...`
- 原始生成文件保留在 `output/xhs-<topic>-<YYYYMMDD>/`
