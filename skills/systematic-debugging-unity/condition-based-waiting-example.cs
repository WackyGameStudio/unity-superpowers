using System;
using System.Collections;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;

/// <summary>
/// Condition-based waiting helpers for UnityTest coroutines.
/// Copy into a PlayMode test assembly when a test waits for scene, physics,
/// animation, async loading, or generated object state.
/// </summary>
public static class UnityConditionWait
{
    public static IEnumerator Until(
        Func<bool> condition,
        string description,
        float timeoutSeconds = 5f)
    {
        var start = Time.realtimeSinceStartup;

        while (!condition())
        {
            if (Time.realtimeSinceStartup - start > timeoutSeconds)
            {
                Assert.Fail($"Timeout waiting for {description} after {timeoutSeconds:0.00}s");
            }

            yield return null;
        }
    }

    public static IEnumerator UntilFixed(
        Func<bool> condition,
        string description,
        float timeoutSeconds = 5f)
    {
        var start = Time.realtimeSinceStartup;

        while (!condition())
        {
            if (Time.realtimeSinceStartup - start > timeoutSeconds)
            {
                Assert.Fail($"Timeout waiting for {description} after {timeoutSeconds:0.00}s");
            }

            yield return new WaitForFixedUpdate();
        }
    }

    public static IEnumerator UntilObjectExists(
        string objectName,
        float timeoutSeconds = 5f)
    {
        // Smoke-test helper only. Prefer direct references or scene queries when possible.
        // GameObject.Find is name-dependent and does not find inactive objects.
        yield return Until(
            () => GameObject.Find(objectName) != null,
            $"GameObject '{objectName}' to exist",
            timeoutSeconds);
    }

    public static IEnumerator UntilAnimatorState(
        Animator animator,
        string stateName,
        int layer = 0,
        float timeoutSeconds = 5f)
    {
        yield return Until(
            () => animator.GetCurrentAnimatorStateInfo(layer).IsName(stateName),
            $"Animator '{animator.name}' to enter state '{stateName}'",
            timeoutSeconds);
    }
}

public sealed class UnityConditionWaitExampleTests
{
    [UnityTest]
    public IEnumerator Rigidbody_DropsBelowStart_AfterPhysicsRuns()
    {
        var go = new GameObject("Rigidbody test body");
        go.AddComponent<Rigidbody>();
        var startY = go.transform.position.y;

        try
        {
            yield return UnityConditionWait.UntilFixed(
                () => go.transform.position.y < startY,
                "Rigidbody to move during a fixed physics step");

            Assert.Less(go.transform.position.y, startY);
        }
        finally
        {
            UnityEngine.Object.Destroy(go);
        }
    }
}

// Usage example:
//
// BEFORE (flaky):
// yield return new WaitForSeconds(0.2f);
// Assert.IsTrue(player.GetComponent<PlayerMotor>().IsGrounded);
//
// AFTER (condition-based):
// yield return UnityConditionWait.UntilFixed(
//     () => player.GetComponent<PlayerMotor>().IsGrounded,
//     "player to become grounded after spawn");
// Assert.IsTrue(player.GetComponent<PlayerMotor>().IsGrounded);
