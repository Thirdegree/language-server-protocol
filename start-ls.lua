function start_lsp(name)
    vim.lsp.start({
        name = name,
        cmd = { 'python', 'examples/' .. name },
        root_dir = vim.fs.dirname(vim.fs.find({ 'pyproject.toml' }, { upward = true })[1]),
    })
    vim.keymap.set('i', 'mmmm', vim.lsp.buf.completion, {})
end
