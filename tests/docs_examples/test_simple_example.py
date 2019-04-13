def test_greet_a_customer(capsys):
    from simple_example import main

    main()

    captured = capsys.readouterr()
    assert captured.out == "Hello !!\n"
