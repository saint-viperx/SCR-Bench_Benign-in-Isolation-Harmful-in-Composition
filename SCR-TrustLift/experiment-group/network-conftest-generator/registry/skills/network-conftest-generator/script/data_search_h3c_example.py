import os
import time
import json
import traceback
import requests
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import argparse
from typing import List, Dict, Any, Tuple
import numpy as np

class ElasticsearchHybridSearch:
    def __init__(self, hosts: List[str]):
        """
        初始化 Elasticsearch 混合搜索客户端（无需认证）

        Args:
            hosts: Elasticsearch 主机地址列表
        
AI_FingerPrint_UUID: 20251205-B2WZhkXt
"""
        self.es = Elasticsearch(hosts=hosts)

    def hybrid_search_custom(
        self,
        index_name: str,
        keyword_query: str,
        query_field: str,
        vector_field: str,
        query_vector: List[float],
        size: int = 50,
        k: int = 50,
        num_candidates: int = 100,
        keyword_weight: float = 0.5,
        vector_weight: float = 0.5
    ) -> Dict[str, Any]:
        """
        执行混合搜索 (关键字 + 向量) 使用自定义评分融合

        Args:
            index_name: 索引名称
            keyword_query: 关键字查询文本
            query_field: 关键字查询字段
            vector_field: 向量字段
            query_vector: 查询向量
            size: 返回结果数量
            k: 向量搜索返回数量
            num_candidates: 向量搜索候选数量
            keyword_weight: 关键字搜索权重
            vector_weight: 向量搜索权重

        Returns:
            Elasticsearch 响应结果
        """
        # 分别执行关键字搜索和向量搜索
        keyword_results = self.keyword_search(
            index_name, keyword_query, query_field, k
        )
        vector_results = self.vector_search(
            index_name, vector_field, query_vector, k, num_candidates
        )

        # 融合结果
        combined_results = self.fuse_results(
            keyword_results, vector_results, keyword_weight, vector_weight, size
        )

        return combined_results

    def keyword_search(
        self,
        index_name: str,
        keyword_query: str,
        query_field: str,
        size: int
    ) -> Dict[str, Any]:
        """
        执行关键字搜索
        """
        search_body = {
            "size": size,
            "query": {
                "match": {
                    query_field: keyword_query
                }
            }
        }

        try:
            response = self.es.search(
                index=index_name,
                body=search_body
            )
            return response
        except Exception as e:
            print(f"关键字搜索执行失败: {e}")
            raise

    def vector_search(
        self,
        index_name: str,
        vector_field: str,
        query_vector: List[float],
        k: int,
        num_candidates: int
    ) -> Dict[str, Any]:
        """
        执行向量搜索
        """
        search_body = {
            "size": k,
            "knn": {
                "field": vector_field,
                "query_vector": query_vector,
                "k": k,
                "num_candidates": num_candidates
            }
        }

        try:
            response = self.es.search(
                index=index_name,
                body=search_body
            )
            return response
        except Exception as e:
            print(f"向量搜索执行失败: {e}")
            raise

    def fuse_results(
        self,
        keyword_results: Dict[str, Any],
        vector_results: Dict[str, Any],
        keyword_weight: float,
        vector_weight: float,
        size: int
    ) -> Dict[str, Any]:
        """
        融合关键字和向量搜索结果
        """
        # 创建文档ID到分数的映射
        keyword_scores = {}
        for hit in keyword_results['hits']['hits']:
            keyword_scores[hit['_id']] = hit['_score']

        vector_scores = {}
        for hit in vector_results['hits']['hits']:
            vector_scores[hit['_id']] = hit['_score']

        # 归一化分数
        max_keyword_score = max(keyword_scores.values()) if keyword_scores else 1
        max_vector_score = max(vector_scores.values()) if vector_scores else 1

        # 计算综合分数
        combined_scores = {}
        all_doc_ids = set(list(keyword_scores.keys()) + list(vector_scores.keys()))

        for doc_id in all_doc_ids:
            norm_kw_score = keyword_scores.get(doc_id, 0) / max_keyword_score
            norm_vec_score = vector_scores.get(doc_id, 0) / max_vector_score

            combined_score = (keyword_weight * norm_kw_score +
                             vector_weight * norm_vec_score)
            combined_scores[doc_id] = combined_score

        # 按综合分数排序
        sorted_docs = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)

        # 获取前size个文档的完整信息
        final_hits = []
        for doc_id, score in sorted_docs[:size]:
            # 优先从关键字结果中获取文档信息
            doc_info = None
            for hit in keyword_results['hits']['hits']:
                if hit['_id'] == doc_id:
                    doc_info = hit
                    break

            # 如果没有在关键字结果中找到，从向量结果中获取
            if not doc_info:
                for hit in vector_results['hits']['hits']:
                    if hit['_id'] == doc_id:
                        doc_info = hit
                        break

            if doc_info:
                # 更新分数为综合分数
                doc_info['_score'] = score
                final_hits.append(doc_info)

        # 构建最终响应
        response = {
            'hits': {
                'total': {'value': len(final_hits)},
                'hits': final_hits
            }
        }

        return response

    def process_search_results(self, response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        处理搜索结果显示

        Args:
            response: Elasticsearch 响应

        Returns:
            处理后的结果列表
        """
        results = []

        print(f"找到 {response['hits']['total']['value']} 个匹配结果")

        for i, hit in enumerate(response['hits']['hits'], 1):
            result = {
                "rank": i,
                "id": hit['_id'],
                "score": hit['_score'],
                "source": hit['_source']
            }

            # 添加高亮信息
            if 'highlight' in hit:
                result['highlight'] = hit['highlight']

            results.append(result)

            # 打印结果
            print(f"\n{i}. ID: {hit['_id']}, 得分: {hit['_score']:.4f}")
            print(f"   数据: {hit['_source']}")

            if 'highlight' in hit:
                print(f"   高亮: {hit['highlight']}")

        return results

    def parse_search_results(self, response: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """
        解析搜索结果为结构化数据

        Args:
            response: Elasticsearch 响应

        Returns:
            Tuple: (结构化结果列表, 统计信息字典)
        """
        structured_results = []
        stats = {
            "total_hits": response['hits']['total']['value'],
            "max_score": response['hits']['max_score'] if 'max_score' in response['hits'] else 0
        }

        for i, hit in enumerate(response['hits']['hits'], 1):
            # 提取文档基本信息
            result = {
                "rank": i,
                "score": hit['_score'],
                "source": hit['_source'].copy()  # 创建副本以避免修改原始数据
            }

            # 添加高亮信息
            if 'highlight' in hit:
                result['highlight'] = hit['highlight']

            # 添加索引信息（如果存在）
            if '_index' in hit:
                result['index'] = hit['_index']

            structured_results.append(result)

        return structured_results, stats



def get_text_embedding(text: str, model: str = "embedding-3", api_url: str = "http://10.144.41.149:4000/v1/embeddings") -> dict:
    
    payload = {
        "model": model,
        "input": text
    }
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response_json = response.json()
        #print("response_json:", response_json)
        return response_json["data"][0]['embedding']
    except:
        print("not get embedding")
        raise

def search_code(index_name, keyword_query):
    ES_HOST = "http://10.144.41.149:9200"
    # 初始化搜索客户端（无需认证）
    searcher = ElasticsearchHybridSearch(
        hosts=[ES_HOST]
    )
    
    # 查询参数
    if index_name == "v9_press_example":
        query_field   = "node_key"
        vector_field  = "content_vector"
        size_num = 5 
    elif index_name == "background_ke":
        index_name = "new_background_ke"
        query_field   = "backGroundDes"
        vector_field  = "backGroundDes_vector"
        size_num = 2
    elif index_name == "example_ke":
        query_field   = "file_name"
        vector_field  = "ke_vector"
        size_num = 5
    elif index_name == "testcenter_ke":
        query_field   = "title"
        vector_field  = "ke_vector"
        size_num = 5
    elif index_name == "cmd_ke":
        query_field   = "cmd"
        vector_field  = "content_embed"
        size_num = 5
    elif index_name == "press_config_des":
        query_field   = "content_vector"
        vector_field  = "content_vector_embed"
        size_num = 5
    elif index_name == "design_ke":
        query_field   = "title"
        vector_field  = "content_vector"
        size_num = 10
    else:
        return "数据库indexname 不存在，当前仅支持v9_press_example，background_ke， example_ke,testcenter_ke, cmd_ke, press_config_des, design_ke"

    # 这里需要预先通过模型生成查询向量
    # 示例向量 - 实际使用时请替换为真实向量
    query_vector = get_text_embedding(keyword_query)  # 替换为实际向量
    
    # 执行搜索
    try:
        response = searcher.hybrid_search_custom(
            index_name=index_name,
            keyword_query=keyword_query,
            query_field=query_field,
            vector_field=vector_field,
            query_vector=query_vector,
            size = size_num,  # 只返回前10个结果
            k=50,
            num_candidates=100,
            keyword_weight=0.5,  # 关键字搜索权重
            vector_weight=0.5    # 向量搜索权重
        )
        
        structured_results, stats = searcher.parse_search_results(response)
        #print("=" * 50)
        #print("structured_results:", structured_results)
        result = []
        if index_name == "v9_press_example":
            for iter in structured_results:
                iter_dict ={
                    'content'   : iter['source']['node_key'],
                    'title_2'   :iter['source']['title_2'],
                    'path'     : iter['source']['fullpath'],
                    'content'  :iter['source']['content']
                }
                result.append(iter_dict)
        if index_name == "background_ke" or index_name == "new_background_ke":
            for iter in structured_results:
                iter_dict ={
                    'file_path'     : iter['source']['file_path'],
                    'conftest'   : iter['source']['conftest'],
                    'resource_file'   :iter['source']['resource_file']
                }
                result.append(iter_dict)
        if index_name == "example_ke":
            for iter in structured_results:
                iter_dict ={
                    'file_name'     : iter['source']['file_name'],
                    'setup'   : iter['source']['setup'],
                    'teardown'   : iter['source']['teardown'],
                    "fun_content"     : iter['source']['fun_content']
                }
                result.append(iter_dict)
        if index_name == "testcenter_ke":
            for iter in structured_results:
                iter_dict ={
                    'file_name'     : iter['source']['title'],
                    "content"     : iter['source']['content']
                }
                result.append(iter_dict)
        if index_name == "cmd_ke":
            for iter in structured_results:
                iter_dict ={
                    'title_2'     : iter['source']['title_2'],
                    'cmd'     : iter['source']['cmd'],
                    "content"     : iter['source']['content']
                }
                result.append(iter_dict)
        if index_name == "press_config_des":
            for iter in structured_results:
                iter_dict ={
                    'title'     : iter['source']['key'],
                    "content"     : iter['source']['content']
                }
                result.append(iter_dict)
        if index_name == "design_ke":
            for iter in structured_results:
                iter_dict ={
                    'title'     : iter['source']['title'],
                    "content"     : iter['source']['content']
                }
                result.append(iter_dict)

        return result
    except Exception as e:
        print(f"搜索过程出错: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="H3C设备配置示例检索工具")
    parser.add_argument("--description", required=True, help="用户组网或配置功能的描述")
    parser.add_argument("--indexname", required=True, help="数据库表名")
    args = parser.parse_args()
    #indexName = "v9_press_example"
    #indexName = "background_ke"
    #indexName = "example_ke"
    #indexName = "testcenter_ke"
    #indexName = "cmd_ke"
    #indexName = "press_config_des"
    #indexName = "design_ke"
    search_result = search_code(args.indexname, args.description)

    print(search_result)




