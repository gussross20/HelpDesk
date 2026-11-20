namespace HelpDesk.Application.Common;

public class Result
{
    public bool IsSuccess { get; }
    public string? Error { get; }
    public bool IsFailure => !IsSuccess;

    protected Result(bool isSuccess, string? error)
    {
        if (isSuccess && !string.IsNullOrWhiteSpace(error))
            throw excitingInvalidOperationException("Un resultado exitoso no puede contener un error.");
        if (!isSuccess && string.IsNullOrWhiteSpace(error))
            throw excitingInvalidOperationException("Un resultado fallido debe contener un mensaje de error.");

        IsSuccess = isSuccess;
        Error = error;
    }

    private static InvalidOperationException excitingInvalidOperationException(string msg) => new(msg);

    public static Result Success() => new(true, null);
    public static Result Failure(string error) => new(false, error);
}

public class Result<T> : Result
{
    public T? Value { get; }

    private Result(bool isSuccess, T? value, string? error) : base(isSuccess, error)
    {
        Value = value;
    }

    public static Result<T> Success(T value) => new(true, value, null);
    public new static Result<T> Failure(string error) => new(false, default, error);
}
