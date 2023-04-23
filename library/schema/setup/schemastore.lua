local geno_schemas = {
  schemas = vim.list_extend(
    {
      {
        description = 'Modules Schema for Genotyper',
        fileMatch = { 'modules.lib.yaml' },
        name = 'modules_schema.json',
        url = 'https://github.com/TechnocultureResearch/genodatalib/blob/dev/library/schema/modules_schema.json',
      },

      {
        description = 'Tools Schema for Genotyper',
        fileMatch = { 'tools.lib.yaml' },
        name = 'tools_schema.json',
        url = 'https://github.com/TechnocultureResearch/genodatalib/blob/dev/library/schema/tools_schema.json',
      },

      {
        description = 'Nodes Schema for Genotyper',
        fileMatch = { 'nodes.lib.yaml' },
        name = 'nodes_schema.json',
        url = 'https://github.com/TechnocultureResearch/genodatalib/blob/dev/library/schema/nodes_schema.json',
      },

      {
        description = 'Behaviour Trees Schema for Genotyper',
        fileMatch = { '*.tree.yaml' },
        name = 'trees_schema.json',
        url = 'https://github.com/TechnocultureResearch/genodatalib/blob/dev/library/schema/trees_schema.json',
      },

      {
        description = 'Workflow Schema for Genotyper',
        fileMatch = { '*.wflow.yaml' },
        name = 'workflows_schema.json',
        url = 'https://github.com/TechnocultureResearch/genodatalib/blob/dev/library/schema/workflows_schema.json',
      },
    },
    require('schemastore').json.schemas()),
  validate = { enable = true },
}

require('lspconfig')['jsonls'].setup{
    on_attach = on_attach,
    flags = lsp_flags,
    settings = {
        json = geno_schemas,
    },
}

require('lspconfig')['yamlls'].setup{
    on_attach = on_attach,
    flags = lsp_flags,
    settings = {
        yaml = geno_schemas,
    },
}
