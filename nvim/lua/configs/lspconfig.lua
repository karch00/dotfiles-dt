require("nvchad.configs.lspconfig").defaults()


local servers = {
  -- Webdev
  "html-lsp",
  "css-lsp" ,
  "eslint-lsp",

  -- Python
  "pyright",

  -- C/C++/C#
  "clangd",

  -- Linux
  "bash-language-server",
  "qmlls",

  -- LUA
  "lua-language-server",

  -- Data files
  "jsonlint",
  "yamllint"
}
vim.lsp.enable(servers)



-- read :h vim.lsp.config for changing options of lsp servers 

