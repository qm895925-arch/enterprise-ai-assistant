import numpy as np

from app.services.embedding_service import EmbeddingService


def cosine_similarity(
    vector_a: list[float],
    vector_b: list[float],
) -> float:
    a = np.array(vector_a)
    b = np.array(vector_b)

    return float(
        np.dot(a, b)
        / (np.linalg.norm(a) * np.linalg.norm(b))
    )


embedding_service = EmbeddingService()

texts = [
    "公司员工每年享有带薪年假。",
    "正式员工每年可以申请年假。",
    "公司使用三维装箱算法优化运输车辆。",
]

vectors = [
    embedding_service.embed_text(text)
    for text in texts
]

print("=== Cosine Similarity ===")

for i in range(len(texts)):
    for j in range(i + 1, len(texts)):
        similarity = cosine_similarity(
            vectors[i],
            vectors[j],
        )

        print(
            f"\nText {i + 1} vs Text {j + 1}"
        )
        print(f"Similarity: {similarity:.4f}")
        print(f"Text {i + 1}: {texts[i]}")
        print(f"Text {j + 1}: {texts[j]}")