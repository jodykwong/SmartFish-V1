#!/usr/bin/env python3
"""
修复报告自动重复生成问题。

问题：checkReportLockStatus() 函数每15秒检查一次，在某些条件下会重复触发 generateReport()。
解决方案：
1. 添加冷却时间机制，确保报告生成完成后5分钟内不会再次自动触发
2. 修改判断条件，增加更严格的保护
"""

import re

def fix_auto_generate():
    file_path = 'templates/index.html'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 添加冷却时间变量
    old_vars = '''        // 刷新Report Engine日志
        // 检查Report Engine锁定状态并自动生成报告
        let autoGenerateTriggered = false; // 防止重复触发
        
        function checkReportLockStatus() {'''
    
    new_vars = '''        // 刷新Report Engine日志
        // 检查Report Engine锁定状态并自动生成报告
        let autoGenerateTriggered = false; // 防止重复触发
        let lastReportGenerationTime = 0; // 记录上次报告生成时间
        const AUTO_GENERATE_COOLDOWN_MS = 5 * 60 * 1000; // 自动生成冷却时间：5分钟
        
        function checkReportLockStatus() {'''
    
    if old_vars in content:
        content = content.replace(old_vars, new_vars)
        print("✅ 已添加冷却时间变量")
    else:
        print("⚠️ 未找到目标变量定义，可能已经修改过")
    
    # 2. 修改自动触发条件，添加冷却时间检查
    old_condition = '''                    // 如果当前在report页面且还没有触发自动生成且没有正在进行的任务且没有已显示的报告，则自动生成报告
                    if (currentApp === 'report' && !autoGenerateTriggered && !reportTaskId && !hasReport) {
                        autoGenerateTriggered = true;
                        console.log('检测到锁消失且无现有报告，自动开始生成报告');
                        setTimeout(() => {
                            generateReport();
                        }, 1000); // 延迟1秒开始生成
                    }'''
    
    new_condition = '''                    // 如果当前在report页面且还没有触发自动生成且没有正在进行的任务且没有已显示的报告
                    // 【修复】添加冷却时间检查，防止报告完成后被重新触发
                    const now = Date.now();
                    const cooldownElapsed = (now - lastReportGenerationTime) > AUTO_GENERATE_COOLDOWN_MS;
                    
                    if (currentApp === 'report' && !autoGenerateTriggered && !reportTaskId && !hasReport && cooldownElapsed) {
                        autoGenerateTriggered = true;
                        lastReportGenerationTime = now; // 记录触发时间
                        console.log('检测到锁消失且无现有报告，冷却时间已过，自动开始生成报告');
                        setTimeout(() => {
                            generateReport();
                        }, 1000); // 延迟1秒开始生成
                    } else if (!cooldownElapsed && !hasReport) {
                        console.log('检测到自动生成条件满足，但仍在冷却时间内，跳过自动生成');
                    }'''
    
    if old_condition in content:
        content = content.replace(old_condition, new_condition)
        print("✅ 已添加冷却时间检查条件")
    else:
        print("⚠️ 未找到目标条件语句，可能已经修改过")
    
    # 3. 在报告完成时更新 lastReportGenerationTime
    # 找到报告完成的地方并更新时间
    old_completed = '''                    if (data.task.status === 'completed') {
                        stopProgressPolling();
                        showMessage('报告生成完成！', 'success');
                        
                        // 自动显示报告
                        viewReport(taskId);
                        reportAutoPreviewLoaded = true;
                        
                        // 重置自动生成标志，允许下次有新内容时自动生成
                        autoGenerateTriggered = false;
                        reportTaskId = null;
                        setGenerateButtonState(false);
                    }'''
    
    new_completed = '''                    if (data.task.status === 'completed') {
                        stopProgressPolling();
                        showMessage('报告生成完成！', 'success');
                        
                        // 自动显示报告
                        viewReport(taskId);
                        reportAutoPreviewLoaded = true;
                        
                        // 【修复】更新完成时间，启动冷却期防止重复触发
                        lastReportGenerationTime = Date.now();
                        // 重置自动生成标志，但由于冷却时间的保护，不会立即重新触发
                        autoGenerateTriggered = false;
                        reportTaskId = null;
                        setGenerateButtonState(false);
                    }'''
    
    if old_completed in content:
        content = content.replace(old_completed, new_completed)
        print("✅ 已在报告完成时更新冷却时间")
    else:
        print("⚠️ 未找到报告完成处理代码，可能已经修改过")
    
    # 保存修改后的文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n🎉 修复完成！报告自动生成现在有5分钟冷却时间保护。")
    print("   - 报告完成后5分钟内不会自动重新触发")
    print("   - 手动点击生成按钮不受影响")

if __name__ == '__main__':
    fix_auto_generate()
