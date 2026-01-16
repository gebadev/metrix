/**
 * metrix - Unit Converter JavaScript
 * API連携と動的UI更新を担当
 */

// DOM要素の取得
const categorySelect = document.getElementById('category');
const valueInput = document.getElementById('value');
const fromUnitSelect = document.getElementById('from-unit');
const toUnitSelect = document.getElementById('to-unit');
const convertBtn = document.getElementById('convert-btn');
const batchConvertBtn = document.getElementById('batch-convert-btn');
const resultSection = document.getElementById('result-section');
const resultContent = document.getElementById('result-content');
const batchResultSection = document.getElementById('batch-result-section');
const batchResultContent = document.getElementById('batch-result-content');
const errorSection = document.getElementById('error-section');
const errorMessage = document.getElementById('error-message');

// 初期化処理
document.addEventListener('DOMContentLoaded', () => {
    // 初期カテゴリ（length）の単位をロード
    loadUnits('length');

    // イベントリスナーの設定
    categorySelect.addEventListener('change', handleCategoryChange);
    convertBtn.addEventListener('click', handleConvert);
    batchConvertBtn.addEventListener('click', handleBatchConvert);

    // Enterキーで変換を実行
    valueInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleConvert();
        }
    });
});

/**
 * カテゴリ変更時の処理
 */
async function handleCategoryChange() {
    const category = categorySelect.value;
    await loadUnits(category);
    // エラーと結果をクリア
    hideError();
    hideResult();
    hideBatchResult();
}

/**
 * 指定されたカテゴリの単位一覧を取得してドロップダウンを更新
 * @param {string} category - カテゴリ名 (length, weight, temperature)
 */
async function loadUnits(category) {
    try {
        showLoading(true);

        const response = await fetch(`/api/units/${category}`);

        if (!response.ok) {
            throw new Error(`Failed to load units: ${response.statusText}`);
        }

        const data = await response.json();

        // ドロップダウンをクリア
        fromUnitSelect.innerHTML = '';
        toUnitSelect.innerHTML = '';

        // 単位オプションを追加
        data.units.forEach((unit, index) => {
            const fromOption = new Option(unit.name, unit.code);
            const toOption = new Option(unit.name, unit.code);

            fromUnitSelect.add(fromOption);
            toUnitSelect.add(toOption);

            // デフォルト選択（from: 最初の単位、to: 2番目の単位）
            if (index === 0) {
                fromOption.selected = true;
            }
            if (index === 1) {
                toOption.selected = true;
            }
        });

    } catch (error) {
        showError(`単位の読み込みに失敗しました: ${error.message}`);
    } finally {
        showLoading(false);
    }
}

/**
 * 変換ボタンクリック時の処理
 */
async function handleConvert() {
    // 入力値のバリデーション
    if (!validateInput()) {
        return;
    }

    // エラーと前の結果をクリア
    hideError();
    hideResult();
    hideBatchResult();

    try {
        showLoading(true);

        // リクエストデータの準備
        const requestData = {
            value: parseFloat(valueInput.value),
            from_unit: fromUnitSelect.value,
            to_unit: toUnitSelect.value,
            category: categorySelect.value
        };

        // API呼び出し
        const response = await fetch('/api/convert', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });

        const data = await response.json();

        if (!response.ok || !data.success) {
            throw new Error(data.error || 'Conversion failed');
        }

        // 結果を表示
        displayResult(data);

    } catch (error) {
        showError(`変換に失敗しました: ${error.message}`);
    } finally {
        showLoading(false);
    }
}

/**
 * 一括変換ボタンクリック時の処理
 */
async function handleBatchConvert() {
    // 入力値のバリデーション（to_unitは不要）
    if (!validateBatchInput()) {
        return;
    }

    // エラーと前の結果をクリア
    hideError();
    hideResult();
    hideBatchResult();

    try {
        showBatchLoading(true);

        // リクエストデータの準備
        const requestData = {
            value: parseFloat(valueInput.value),
            from_unit: fromUnitSelect.value,
            category: categorySelect.value
            // to_units は省略（全単位に変換）
        };

        // API呼び出し
        const response = await fetch('/api/convert/batch', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });

        const data = await response.json();

        if (!response.ok || !data.success) {
            throw new Error(data.error || 'Batch conversion failed');
        }

        // 結果を表示
        displayBatchResult(data);

    } catch (error) {
        showError(`一括変換に失敗しました: ${error.message}`);
    } finally {
        showBatchLoading(false);
    }
}

/**
 * 共通の入力値バリデーション
 * @returns {boolean} - バリデーション結果
 */
function validateCommonInput() {
    const value = valueInput.value.trim();

    // 空チェック
    if (value === '') {
        showError('値を入力してください');
        valueInput.focus();
        return false;
    }

    // 数値チェック
    const numValue = parseFloat(value);
    if (isNaN(numValue)) {
        showError('有効な数値を入力してください');
        valueInput.focus();
        return false;
    }

    // 無限大チェック
    if (!isFinite(numValue)) {
        showError('有限の数値を入力してください');
        valueInput.focus();
        return false;
    }

    // from_unit選択チェック
    if (!fromUnitSelect.value) {
        showError('変換元の単位を選択してください');
        return false;
    }

    return true;
}

/**
 * 入力値のクライアント側バリデーション
 * @returns {boolean} - バリデーション結果
 */
function validateInput() {
    // 共通バリデーション
    if (!validateCommonInput()) {
        return false;
    }

    // to_unit選択チェック（単一変換のみ）
    if (!toUnitSelect.value) {
        showError('変換先の単位を選択してください');
        return false;
    }

    return true;
}

/**
 * 一括変換用の入力値バリデーション
 * @returns {boolean} - バリデーション結果
 */
function validateBatchInput() {
    // 共通バリデーションのみ（to_unitは不要）
    return validateCommonInput();
}

/**
 * 変換結果を表示
 * @param {Object} data - APIレスポンスデータ
 */
function displayResult(data) {
    // 結果のフォーマット
    const resultText = `
        <div class="result-value">
            <strong>${formatNumber(data.result)}</strong> ${getUnitDisplayName(data.to_unit)}
        </div>
        <div class="result-detail">
            ${formatNumber(data.original_value)} ${getUnitDisplayName(data.from_unit)}
            = ${formatNumber(data.result)} ${getUnitDisplayName(data.to_unit)}
        </div>
    `;

    resultContent.innerHTML = resultText;
    resultSection.style.display = 'block';
}

/**
 * 一括変換結果を表示
 * @param {Object} data - APIレスポンスデータ
 */
function displayBatchResult(data) {
    // ヘッダー情報
    let resultHTML = `
        <div class="batch-result-header">
            <p><strong>${formatNumber(data.original_value)} ${getUnitDisplayName(data.from_unit)}</strong> を他の単位に変換:</p>
        </div>
    `;

    // 結果テーブル
    if (data.results.length > 0) {
        resultHTML += '<table class="batch-result-table">';
        resultHTML += '<thead><tr><th>単位</th><th>変換結果</th></tr></thead>';
        resultHTML += '<tbody>';

        data.results.forEach(result => {
            resultHTML += `
                <tr>
                    <td>${getUnitDisplayName(result.to_unit)}</td>
                    <td><strong>${formatNumber(result.value)}</strong></td>
                </tr>
            `;
        });

        resultHTML += '</tbody></table>';
    } else {
        resultHTML += '<p>変換結果がありません。</p>';
    }

    // 失敗した単位がある場合は表示
    if (data.failed_units && data.failed_units.length > 0) {
        resultHTML += `
            <div class="batch-result-warning">
                <p><strong>警告:</strong> 以下の単位への変換に失敗しました: ${data.failed_units.join(', ')}</p>
            </div>
        `;
    }

    batchResultContent.innerHTML = resultHTML;
    batchResultSection.style.display = 'block';
}

/**
 * 数値をフォーマット（小数点以下の桁数を調整）
 * @param {number} num - フォーマットする数値
 * @returns {string} - フォーマットされた数値文字列
 */
function formatNumber(num) {
    // 整数の場合はそのまま表示
    if (Number.isInteger(num)) {
        return num.toString();
    }

    // 小数の場合は最大6桁まで表示（末尾のゼロは削除）
    return parseFloat(num.toFixed(6)).toString();
}

/**
 * 単位コードから表示名を取得
 * @param {string} unitCode - 単位コード
 * @returns {string} - 単位の表示名
 */
function getUnitDisplayName(unitCode) {
    // 選択中の単位から表示名を探す
    const option = [...fromUnitSelect.options, ...toUnitSelect.options].find(
        opt => opt.value === unitCode
    );
    return option ? option.text : unitCode;
}

/**
 * エラーメッセージを表示
 * @param {string} message - エラーメッセージ
 */
function showError(message) {
    errorMessage.textContent = message;
    errorSection.style.display = 'block';
    resultSection.style.display = 'none';
}

/**
 * エラーメッセージを非表示
 */
function hideError() {
    errorSection.style.display = 'none';
    errorMessage.textContent = '';
}

/**
 * 結果を非表示
 */
function hideResult() {
    resultSection.style.display = 'none';
    resultContent.innerHTML = '';
}

/**
 * 一括変換結果を非表示
 */
function hideBatchResult() {
    batchResultSection.style.display = 'none';
    batchResultContent.innerHTML = '';
}

/**
 * ローディング状態を管理
 * @param {boolean} loading - ローディング中かどうか
 */
function showLoading(loading) {
    if (loading) {
        convertBtn.disabled = true;
        convertBtn.textContent = 'Converting...';
        convertBtn.classList.add('loading');
    } else {
        convertBtn.disabled = false;
        convertBtn.textContent = 'Convert';
        convertBtn.classList.remove('loading');
    }
}

/**
 * 一括変換のローディング状態を管理
 * @param {boolean} loading - ローディング中かどうか
 */
function showBatchLoading(loading) {
    if (loading) {
        batchConvertBtn.disabled = true;
        batchConvertBtn.textContent = 'Converting...';
        batchConvertBtn.classList.add('loading');
    } else {
        batchConvertBtn.disabled = false;
        batchConvertBtn.textContent = 'Batch Convert';
        batchConvertBtn.classList.remove('loading');
    }
}
