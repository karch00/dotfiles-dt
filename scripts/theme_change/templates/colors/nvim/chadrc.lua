-- This file needs to have same structure as nvconfig.lua 
-- https://github.com/NvChad/ui/blob/v3.0/lua/nvconfig.lua
-- Please read that file to know all available options :( 

local M = {}

M.base46 = {
	changed_themes = {
    nord = {
      base_30 = {
        white = "#%c7%",
        black = "#%c0%",
        darker_black = "#%c20%",
        black2 = "#%c21%",
        one_bg = "#%c22%",
        one_bg2 = "#%c23%",
        one_bg3 = "#%c24%",
        grey = "#%c25%",
        grey_fg = "#%c26%",
        grey_fg2 = "#%c27%",
        light_grey = "#%c28%",
        red = "#%c1%",
        baby_pink = "#%c29%",
        pink = "#%c30%",
        line = "#%c31%",
        green = "#%c2%",
        vibrant_green = "#%c10%",
        nord_blue = "#%c32%",
        blue = "#%c4%",
        seablue = "#%c33%",
        yellow = "#%c3%",
        sun = "#%c34%",
        purple = "#%c5%",
        dark_purple = "#%c35%",
        teal = "#%c36%",
        orange = "#%c37%",
        cyan = "#%c6%",

        statusline_bg = "#%c38%",
        lightbg = "#%c39%",
        pmenu_bg = "#%c40%",
        folder_bg = "#%c41%"
      },
      base_16 = {
        base00 = "#%c0%",
        base01 = "#%c21%",
        base02 = "#%c24%",
        base03 = "#%c23%",
        base04 = "#%c22%",
        base05 = "#%c7%",
        base06 = "#%c15%",
        base07 = "#%c39%",
        base08 = "#%c1%",
        base09 = "#%c42%",
        base0A = "#%c3%",
        base0B = "#%c2%",
        base0C = "#%c4%",
        base0D = "#%c4%",
        base0E = "#%c5%",
        base0F = "#%c39%"
      },
    },
  },
  theme = "nord"
}

return M
