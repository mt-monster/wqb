# Field Profile: fundamental72 (DEU)

**Generated**: 2026-11-15 18:38:43  
**Dataset**: fundamental72 (Comprehensive Fundamental Data)  
**Region**: DEU (Germany)  
**Universe**: TOP500  
**Total Fields**: 1031  
**Data Source**: Platform API (get_datafields) + Local DB (get_field_catalog)

---

## Executive Summary

⚠️ **CRITICAL FINDING**: All 1031 fields in fundamental72 have **coverage = 0** for DEU region.

This indicates that while the dataset is technically available for DEU (fieldCount=1031 in dataset catalog), there is **no actual data coverage** for German stocks in the TOP500 universe. This is a **data availability issue**, not a signal quality issue.

**Key Statistics**:
- Fields with coverage > 0: **0** (0%)
- Fields with userCount > 0: **0** (0.0%)
- VECTOR fields: **684** (66.3%)
- MATRIX fields: **347** (33.7%)

**Recommendation**: This dataset is **not viable for DEU atom mining** due to zero data coverage. Consider:
1. Using GLB region where coverage is substantial (0.15-0.93 for many fields)
2. Verifying if fundamental72 data exists for DEU under different universes or delays
3. Focusing on alternative fundamental datasets with actual DEU coverage

---

## Field Family Analysis

### Tower-Relevant Families (FUNDAMENTAL Tower - requires 3 factors)

The following families share economic mechanisms and can contribute to FUNDAMENTAL tower illumination:

| Family | Mechanism | Field Count | Tower Relevant | Status |
|--------|-----------|-------------|----------------|--------|
| **working_capital** | 营运资本管理效率 | ~92 | ✓ Yes | **BLOCKED** (coverage=0) |
| **capital_structure** | 资本结构与财务杠杆 | ~155 | ✓ Yes | **BLOCKED** (coverage=0) |
| **asset_quality** | 资产质量与减值 | ~37 | ✓ Yes | **BLOCKED** (coverage=0) |
| **fixed_assets** | 固定资产密集度 | ~110 | ✓ Yes | **BLOCKED** (coverage=0) |
| **cash_flow** | 现金流生成能力 | ~25 | ✓ Yes | **BLOCKED** (coverage=0) |

**Tower Illumination Potential**: 5 mechanism-bound families identified, but all blocked by zero coverage.

### Probe-Level Families (No Mechanism Binding)

These families lack shared economic mechanisms or are industry-specific:

| Family | Description | Field Count | Probe Level |
|--------|-------------|-------------|-------------|
| banking_specific | 银行业专用（存款/贷款/同业） | ~100 | ✓ Yes |
| insurance_specific | 保险业专用 | ~15 | ✓ Yes |
| real_estate_specific | 房地产专用 | ~30 | ✓ Yes |
| pension | 养老金负债 | ~17 | ✓ Yes |
| tax | 税务负债与递延 | ~21 | No |

---

## Priority Fields (userCount > 0)

Despite zero coverage, 0 fields have been used by other researchers (userCount > 0). These represent fields that *would* be viable if data existed:

| Field ID | Type | Coverage | User Count | Alpha Count | Description |
|----------|------|----------|------------|-------------|-------------|

**Note**: All priority fields show coverage=0 for DEU. userCount reflects global usage across all regions.

---

## Excluded Fields

**Total Excluded**: 1031 fields (100.0%)

### Exclusion Reasons Summary

| Reason | Count | Percentage |
|--------|-------|------------|
| coverage=0 (DEU无数据覆盖） | 1031 | 100.0% |
| 行业专用/窄账户字段 | 68 | 6.6% |
| 语义重复字段 | 23 | 2.2% |
| 元数据字段 | 39 | 3.8% |

### Sample Excluded Fields

| Field ID | Type | Coverage | Reason |
|----------|------|----------|--------|
| federal_funds_sold_2 | VECTOR | 0.0000 | coverage=0 (DEU无数据覆盖); 行业专用/窄账户字段 |
| fnd72_pit_or_bs_a_bs_add_paid_in_cap | VECTOR | 0.0000 | coverage=0 (DEU无数据覆盖) |
| fnd72_pit_or_bs_a_bs_rental_exp_year_5 | VECTOR | 0.0000 | coverage=0 (DEU无数据覆盖) |
| fnd72_pit_or_bs_q_bs_rental_exp_beyond_year_5 | VECTOR | 0.0000 | coverage=0 (DEU无数据覆盖) |
| interbank_assets_balance | VECTOR | 0.0000 | coverage=0 (DEU无数据覆盖); 行业专用/窄账户字段 |
| marketable_securities_value | VECTOR | 0.0000 | coverage=0 (DEU无数据覆盖) |
| other_interbank_assets_2 | VECTOR | 0.0000 | coverage=0 (DEU无数据覆盖); 行业专用/窄账户字段 |
| reinsurance_receivables_balance_2 | VECTOR | 0.0000 | coverage=0 (DEU无数据覆盖); 行业专用/窄账户字段 |
| fnd72_pit_or_cf_a_cf_cap_expend_prpty_add | VECTOR | 0.0000 | coverage=0 (DEU无数据覆盖) |
| fnd72_s_pit_or_bs_q_2_bs_total_capital_leases | MATRIX | 0.0000 | coverage=0 (DEU无数据覆盖) |
| accumulated_depreciation_value | VECTOR | 0.0000 | coverage=0 (DEU无数据覆盖); 语义重复字段 (base: accumulated_depreciation) |
| fnd72_pit_or_bs_q_notes_receivable | VECTOR | 0.0000 | coverage=0 (DEU无数据覆盖) |
| fnd72_s_pit_or_is_a2_is_pension_category_equities | MATRIX | 0.0000 | coverage=0 (DEU无数据覆盖); 行业专用/窄账户字段 |
| demand_deposits_value_2 | VECTOR | 0.0000 | coverage=0 (DEU无数据覆盖); 行业专用/窄账户字段; 语义重复字段 (base: demand_deposits) |
| other_noncurrent_liabilities_amt | VECTOR | 0.0000 | coverage=0 (DEU无数据覆盖) |

---

## VECTOR Field Dimensionality Reduction Recommendations

For VECTOR fields (684 total), the following reduction operators are recommended based on semantic analysis:

| Operator | Use Case | Field Types |
|----------|----------|-------------|
| **vec_avg** | 平均化处理：适用于余额类字段（如平均资产、平均负债） | Balance sheet items |
| **vec_sum** | 求和聚合：适用于流量类字段（如总收入、总支出） | Income statement / cash flow items |
| **vec_max** | 极值提取：适用于风险类字段（如最大风险敞口） | Risk exposure fields |

**Critical**: VECTOR fields must be reduced before use in alpha expressions. Never use raw VECTOR fields.

### VECTOR Field Examples by Reduction Type

**vec_avg candidates** (balance sheet averages):
- accounts_receivable (average receivables)
- inventory (average inventory)
- total_assets (average assets)

**vec_sum candidates** (flow aggregation):
- capital_expenditures (total capex)
- dividends_paid (total dividends)
- cash_from_operations (total operating cash flow)

**vec_max candidates** (risk exposure):
- contingent_liabilities (maximum contingent exposure)
- credit_lines (maximum available credit)

---

## Designer Hints

### Slow Variable Window Expectations

**Annual Fields** (majority of fundamental72):
- Use `ts_backfill(field, 250)` as baseline (1 trading year)
- For quarterly interpolations, use `ts_backfill(field, 63)` with caution
- Window expectations: 250-504 days for stable slow-moving averages

**Quarterly Fields**:
- Use `ts_backfill(field, 63)` as baseline (1 trading quarter)
- Window expectations: 63-126 days

### Sign Prior & Regional Fingerprint Validation

⚠️ **Cannot validate sign priors for DEU** due to zero coverage. 

**Required validation** (if data becomes available):
1. Cross-sectional rank distribution should be uniform (no extreme concentration)
2. Time-series correlation with price/volume should show expected economic sign
3. Regional fingerprint: Compare DEU field distributions with GLB/EUR counterparts

### gBF (group_backfill) Applicability

**Not applicable for DEU** due to zero coverage. However, for other regions:

- **When to use**: Fields with missing values that need group-level imputation
- **Critical requirement**: gBF **must be stacked on top of ts_backfill**, never used alone
- **Recommended pattern**: `group_backfill(ts_backfill(field, 250), group, 250)`

### Dimension Trap Warnings

**Market cap / price level fields**: fundamental72 is primarily balance sheet data, but if combining with price data:
- **Never** use raw market cap or price levels in arithmetic operations
- **Always** apply `rank()` normalization before cross-sectional comparisons
- **Scale trap**: Market cap varies by orders of magnitude; rank normalization is mandatory

---

## Cross-Region Comparison

| Region | Coverage Status | Viable for Mining |
|--------|----------------|-------------------|
| **DEU** | **0% (all fields)** | **✗ NO** |
| GLB | 15-93% (many fields) | ✓ YES |
| USA | Not tested | Unknown |
| EUR | Not tested | Unknown |

**Recommendation**: Redirect fundamental72 mining efforts to **GLB region** where coverage is substantial.

---

## Alternative Datasets for DEU

Since fundamental72 is not viable for DEU, consider these alternatives:

1. **fundamental6**: Company Fundamental Data for Equity (coverage: 0.4923 for DEU)
2. **fundamental17**: Direct Fundamental Data (coverage: 0.0, but 135 fields)
3. **fundamental89**: Accrual based Earnings Model (coverage: 0.0, but 407 fields)
4. **analyst69**: Fundamental Analyst Estimates (coverage: 0.0, but 292 fields)

**Next Steps**:
1. Verify if any fundamental datasets have non-zero coverage for DEU
2. Run category coverage audit: `python tools/gates/category_coverage_audit.py --region DEU --universe TOP500 --delay 1 --category fundamental`
3. Consider using GLB region for fundamental72 mining instead

---

## Field-Level Detail Table

**Complete field listing**: See `field_catalog_fundamental72_deu.json` for all 1031 fields.

**Key statistics**:
- Total fields: 1031
- VECTOR: 684 (66.3%)
- MATRIX: 347 (33.7%)
- Fields with userCount > 0: 0
- Fields with coverage > 0: 0
- Excluded fields: 1031
- Probe-level fields: 0

---

## Methodology Notes

**Data Sources**:
1. Platform API: `get_datafields(region='DEU', dataset_id='fundamental72', universe='TOP500', delay=1)`
2. Local DB: `get_field_catalog(region='DEU', dataset='fundamental72')`

**Dual-channel verification**: Both sources confirm 1031 fields with coverage=0 for DEU.

**Field-level coverage rule**: Per AGENTS.md, dataset-level coverage is advisory only; field-level coverage (from `/data-fields`) is the authoritative gate. All 1031 fields show coverage=0.

**Mechanism binding test**: Field families were evaluated for shared economic mechanisms. Families without mechanism binding are marked as 'probe-level'.

---

**Profile Status**: **BLOCKED** - fundamental72 is not viable for DEU atom mining due to zero data coverage.
