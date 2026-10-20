#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MİRAT Görev Bazlı Model Yönlendiricisi (v6)
Her görev için birincil model ve bağımsız ikinci oy için farklı aileden bir model.
"""

TASK_ROUTING = {
    'prompt_dev': ['space-bunny-free'],
    'antonym_census': ['deepseek-v4.1-flash', 'qwen3.7-plus'],
    'semantic_fields': ['deepseek-v4.1-flash', 'qwen3.7-plus'],
    'narrative_scenes': ['deepseek-v4.1-flash', 'mimo-v2.6-flash'],
    'cluster_naming': ['gpt-6-luna'],
    # v5 görevleri (geriye dönük uyumluluk)
    'hypothesis_proposer': ['gpt-6-luna', 'qwen3.7-plus'],
    'hypothesis_critic': ['glm-5.3-flash', 'qwen3.8-flash'],
    'qa_assistant': ['deepseek-v4-flash', 'qwen3.8-flash'],
    'triangulated_annotation': ['deepseek-v4.1-flash', 'mimo-v2.6-flash', 'muse-spark-1.3-contributor'],
    'testing_and_free': ['space-bunny-free', 'longcat-2.5-preview-free'],
}

DEFAULT_MODEL = 'deepseek-v4.1-flash'


class ModelRouter:
    @staticmethod
    def get_models_for_task(task_name):
        return TASK_ROUTING.get(task_name, [DEFAULT_MODEL])

    @staticmethod
    def get_primary_model(task_name):
        return TASK_ROUTING.get(task_name, [DEFAULT_MODEL])[0]
