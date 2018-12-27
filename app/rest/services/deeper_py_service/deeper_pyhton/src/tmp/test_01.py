from deeper_lite_sim import train, test

if __name__ == "__main__":
    train("Fodors_Zagat", "train.csv", "validation.csv", get_deeper_lite_model_sim)
    test("Fodors_Zagat", "test.csv", "test_predictions.csv", get_deeper_lite_model_sim)

    # train("Cora", "train.csv", "validation.csv", get_deeper_lite_model_sim)
    # test("Cora", "test.csv", "test_predictions.csv", get_deeper_lite_model_sim)
    #
    # train("DBLP_ACM", "train.csv", "validation.csv", get_deeper_lite_model_sim)
    # test("DBLP_ACM", "test.csv", "test_predictions.csv", get_deeper_lite_model_sim)
    #
    # train("DBLP_Scholar", "train.csv", "validation.csv", get_deeper_lite_model_sim)
    # test("DBLP_Scholar", "test.csv", "test_predictions.csv", get_deeper_lite_model_sim)