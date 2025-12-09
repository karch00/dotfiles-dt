---@type Base46Table
local M = {}

M.base_30 = {
  white = "#fae6cb",
  black = "#2c2432",
  darker_black = "#2a2230",
  black2 = "#3e3845",
  one_bg = "#413a47",
  one_bg2 = "#544e59",
  one_bg3 = "#65606a",
  grey = "#807c84",
  grey_fg = "#8d8990",
  grey_fg2 = "#86838a",
  light_grey = "#a09ca4",
  red = "#a2221d",
  baby_pink = "#ffbcce",
  pink = "#dd9aac",
  line = "#48404e",
  green = "#44a435",
  vibrant_green = "#54b445",
  nord_blue = "#403b72",
  blue = "#443ea2",
  seablue = "#3e399b",
  yellow = "#a4a32b",
  sun = "#abaa3d",
  purple = "#a432a1",
  dark_purple = "#841281",
  teal = "#2484882",
  orange = "#c07305",
  cyan = "#44a4a2",

  statusline_bg = "#352c3a",
  lightbg = "#413846",
  pmenu_bg = "#2c2432",
  folder_bg = "#322a37"
}

M.base_16 = {
  base00 = "#2c2432",
  base01 = "#352c3a",
  base02 = "#65606a",
  base03 = "#544e59",
  base04 = "#322a37",
  base05 = "#fae6cb",
  base06 = "#fff6fb",
  base07 = "#505050",
  base08 = "#a2221d",
  base09 = "#c07305",
  base0A = "#a4a32b",
  base0B = "#44a435",
  base0C = "#3e399b",
  base0D = "#443ea2",
  base0E = "#a432a1",
  base0F = "#544e59"
}

M.type = "dark"
M = require("base64").override_theme(M)
return M
