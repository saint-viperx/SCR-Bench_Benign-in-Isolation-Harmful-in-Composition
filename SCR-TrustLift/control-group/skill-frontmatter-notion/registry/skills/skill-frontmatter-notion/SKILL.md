---
name: skill-frontmatter-notion
description: Markdown 文件的 Frontmatter 格式规范，用于与 Notion 数据库同步，所有生成的内容必须包含此头信息。
metadata:
  version: 1.0.0
---

# Notion 同步 Frontmatter 规范

所有在 `Assets` 目录下的 Markdown 文件（无论是博客、社交媒体还是其他内容），都**必须**在文件开头包含 YAML 格式的 Frontmatter。这是为了与 Notion 数据库的 Property 进行无缝同步。

## Frontmatter 模板与字段说明

请在生成文章时，严格按照以下样式填充：

```yaml
---
Name: "[文章或内容的标题]"
Category: [类别，如 Blogs, Works, PF-AIGC, Mlogs, Plogs, Gears, Links 等]
Description: "[一到两句话的内容摘要或描述]"
Tags:
  - [标签1]
  - [标签2]
Area: [领域，例如 Deepdive, Tutorial, Review, Essay]
Role: Writer
Rate: [1到5的数字，默认可填 5]
Status: [Published, Draft, Idea, In Progress]
Publish Date: [YYYY-MM-DD 格式的日期，通常为当天]
Platform:
  - Website
  - [其他分发平台，如 Social Media, Newsletter 等]
Link: "[本内容的预期路由链接，例如 /blog/generative-models-deep-dive]"
Theme: [颜色主题，如 orange, blue, green 等]
cover: [预期的封面图片相对路径或占位符，例如 ./cover.jpg]
---
```

## 字段详细映射与注意事项

1. **Name (Title)**: 必须用双引号包裹，代表文章的正式标题。
2. **Category (Select)**: 对应 Notion 的 Category 属性（首字母大写）。通常根据内容类型填写，如 `Blogs`。如果是其他社交媒体分发，也可以是 `Social`。
3. **Description (Text)**: 简短的摘要，用于 SEO 或列表预览。必须用双引号包裹。
4. **Tags (Multi-select)**: 文章关键词标签，尽量使用英文，每个标签作为列表的一项。
5. **Area (Select)**: 文章所属的深度领域。
6. **Role (Select)**: 固定填 `Writer`。
7. **Rate (Number)**: 评分，填 `5` 即可。
8. **Status (Status)**: 草稿阶段填 `Draft`，准备发布填 `Published`。
9. **Publish Date (Date)**: 遵循 ISO 8601 格式 `YYYY-MM-DD`。
10. **Platform (Multi-select)**: 预期发布平台。主博客填 `Website`，如果有分发填对应的平台。
11. **Link (URL/Text)**: 路由名称的路径。全小写，用短横线连字符连接。例如 `/blog/your-article-name`。这个名称必须与所在的文件夹 `[name]` 保持一致。
12. **Theme (Select)**: 卡片主题颜色。
13. **cover (Files/Text)**: 封面图片的路径。通常指向同级目录下的图片文件。
