# quick_test.py
import requests
import json

def quick_test():
    """Quick test script to verify endpoints are working"""
    base_url = "http://localhost:8000/api"
    headers = {"Content-Type": "application/json"}
    
    test_cases = [
        {
            "name": "Chunk Text",
            "endpoint": "/embedding/chunk/",
            "data": {"text": """This is a test document. It has multiple sentences. We want to chunk it properly.
A Christian holiday signifying the birth of Jesus, Christmas is widely celebrated and enjoyed across the United States and the world. The holiday always falls on 25 December (regardless of the day of the week), and is typically accompanied by decorations, presents, and special meals.
Specifically, the legend behind Christmas (and the one that most children are told) is that Santa Claus, a bearded, hefty, jolly, and red-jacket-wearing old man who lives in the North Pole, spends the year crafting presents with his elves, or small, festive, excited Santa-assistants. All the children who behave throughout the year are admitted to the Good List, and will presumably receive their desired gifts on Christmas, while those who don't behave are placed on the Naughty List, and will presumably (although the matter is determined by parents) receive a lump of coal.
Santa Claus is said to fly around the Christmas sky in a sled powered by his magical reindeer, or cold-resistant, mythically powered, individually named animals, delivering presents to each child's house in the process. Santa is also expected to slide through chimneys to deliver these presents (homes not equipped with chimneys might "leave the front door cracked open"), and children sometimes arrange cookies or other treats on a plate for him to enjoy.
Gifts are placed underneath a Christmas tree, or a pine tree that's decorated with ornaments and/or lights and is symbolic of the holiday. Additionally, smaller gifts may be placed inside a stocking, or a sock-shaped, holiday-specific piece of fabric that's generally hung on the mantle of a fireplace (homes without fireplaces might use the wall). A Christmas tree's ornaments, or hanging, typically spherical decorations, in addition to the mentioned lights, may be accompanied by a star, or a representation of the Star of Jerusalem that the Three Apostles followed while bringing Baby Jesus gifts and honoring him, in the Bible."""}
        },
        {
            "name": "Get Embeddings", 
            "endpoint": "/embedding/encode/",
            "data": {"texts": ["hello world", "test embedding"]}
        }
    ]
    
    print("Testing Embedding API Endpoints\n" + "="*40)
    
    for test in test_cases:
        try:
            print(f"\n{test['name']}:")
            response = requests.post(
                f"{base_url}{test['endpoint']}",
                json=test['data'],
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                print("✅ SUCCESS")
                result = response.json()
                # Print summary of results
                
                for key, value in result.items():
                    print(len(value))
            else:
                print(f"❌ FAILED - Status: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ ERROR - {e}")
    
    # Test comparison
    print(f"\nTesting Comparison:")
    try:
        # First get embeddings
        texts = ["machine learning", "artificial intelligence"]
        embed_response = requests.post(
            f"{base_url}/embedding/encode/",
            json={"texts": texts},
            headers=headers
        )
        
        if embed_response.status_code == 200:
            embeddings = embed_response.json()["embeddings"]
            
            # Then compare
            compare_response = requests.post(
                f"{base_url}/embedding/compare/",
                json={"embedding1": embeddings[0], "embedding2": embeddings[1]},
                headers=headers
            )
            
            if compare_response.status_code == 200:
                similarity = compare_response.json()["cosine_similarity"]
                print(f"✅ Similarity between '{texts[0]}' and '{texts[1]}': {similarity:.4f}")
            else:
                print(f"❌ Comparison failed: {compare_response.status_code}")
        else:
            print(f"❌ Embedding failed: {embed_response.status_code}")
            
    except Exception as e:
        print(f"❌ Comparison test error: {e}")

if __name__ == "__main__":
    quick_test()